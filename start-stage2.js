#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const readline = require('readline');

const PORT = 3000;
const HOST = '0.0.0.0';

/**
 * Findet alle Prozesse, die auf einem bestimmten Port lauschen.
 * Versucht zuerst lsof (schnell), fällt dann auf procfs-Scan zurück (zuverlässig).
 * @param {number} port - Der zu überprüfende Port
 * @returns {Array<{pid, command}>} Array von Prozessen mit PID und Kommandozeile
 */
function findProcessesOnPort(port) {
    try {
        // Versuch 1: lsof (schneller, Linux/macOS)
        const pids = execSync(`lsof -ti:${port}`, { encoding: 'utf8' })
            .trim()
            .split('\n')
            .filter(Boolean);

        return pids.map(pid => ({
            pid: parseInt(pid),
            command: fs.readFileSync(`/proc/${pid}/cmdline`, 'utf8').replace(/\0/g, ' ') || 'unknown'
        }));
    } catch {
        // Fallback: Prozessdatei-System durchsuchen (zuverlässiger)
        const processes = [];
        const portPattern = new RegExp(`--port\\s+${port}|:${port}`, 'i');

        for (let i = 1; i < 65535; i++) {
            try {
                const cmdline = fs.readFileSync(`/proc/${i}/cmdline`, 'utf8').replace(/\0/g, ' ');
                if (portPattern.test(cmdline)) {
                    processes.push({ pid: i, command: cmdline });
                }
            } catch { }
        }
        return processes;
    }
}

/**
 * Fragt den Nutzer interaktiv, ob er Prozesse beenden möchte.
 * Zeigt PID und Kommandozeile aller erkannten Prozesse.
 * @param {Array<{pid, command}>} processes - Prozesse auf dem Port
 * @returns {Promise<boolean>} true wenn ja, false wenn nein
 */
async function askUserToKillProcesses(processes) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    console.log(`\n⚠️  [Stage 2] Port ${PORT} ist bereits belegt!\n`);
    console.log('Laufende Prozesse:');
    processes.forEach(p => {
        const cmdDisplay = p.command.substring(0, 80) + (p.command.length > 80 ? '...' : '');
        console.log(`  • PID ${p.pid}: ${cmdDisplay}`);
    });

    return new Promise(resolve => {
        rl.question('\nMöchtest du diese Prozesse beenden? (ja/nein): ', answer => {
            rl.close();
            const shouldKill = /^(ja|j|y)$/i.test(answer);
            resolve(shouldKill);
        });
    });
}

/**
 * Beendet die angegebenen Prozesse mit SIGTERM.
 * Wartet kurz, damit Prozesse auslaufend beendet werden.
 * @param {Array<{pid, command}>} processes - Zu beendende Prozesse
 */
function killProcesses(processes) {
    console.log('\n[Stage 2] Beende Prozesse...');
    processes.forEach(p => {
        try {
            process.kill(p.pid, 'SIGTERM');
            console.log(`  ✓ PID ${p.pid} beendet`);
        } catch (e) {
            console.log(`  ✗ PID ${p.pid} konnte nicht beendet werden: ${e.message}`);
        }
    });
    // Kurzes Warten für sauberes Beenden
    execSync('sleep 0.5');
}

/**
 * Startet den json-graphql-server mit konfigurierten Host/Port.
 */
function startServer() {
    console.log(`\n[Stage 2] Starte json-graphql-server auf http://${HOST}:${PORT}/\n`);

    const server = spawn('json-graphql-server', [
        'data/contacts.json',
        '--port', PORT.toString(),
        '--host', HOST
    ], {
        cwd: __dirname,
        stdio: 'inherit'
    });

    server.on('error', err => {
        console.error(`[Stage 2] Fehler beim Starten: ${err.message}`);
        process.exit(1);
    });
}

/**
 * Hauptlogik:
 * 1. Prüfe Port auf konfliktive Prozesse
 * 2. Wenn konfrontiert: Nutzer befragen
 * 3. Bei Zustimmung: alte Prozesse beenden
 * 4. Server starten
 */
(async () => {
    const processes = findProcessesOnPort(PORT);

    if (processes.length > 0) {
        const shouldKill = await askUserToKillProcesses(processes);
        if (shouldKill) {
            killProcesses(processes);
        } else {
            console.log('\n[Stage 2] Abbruch: Nutzer hat nicht zugestimmt.\n');
            process.exit(1);
        }
    }

    startServer();
})().catch(err => {
    console.error('[Stage 2] Fehler:', err.message);
    process.exit(1);
});

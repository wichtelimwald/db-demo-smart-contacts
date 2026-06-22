#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const net = require('net');

const PORT = 3000;
const HOST = '0.0.0.0';

/**
 * Prüft portabel, ob ein TCP-Port lokal bereits belegt ist.
 * @param {number} port - Der zu prüfende Port
 * @returns {Promise<boolean>} true wenn belegt, sonst false
 */
function isPortInUse(port) {
    return new Promise(resolve => {
        const socket = net.connect({ host: '127.0.0.1', port });
        socket.once('connect', () => {
            socket.destroy();
            resolve(true);
        });
        socket.once('error', () => {
            resolve(false);
        });
        socket.setTimeout(500, () => {
            socket.destroy();
            resolve(false);
        });
    });
}

function hasCommand(command) {
    try {
        execSync(`command -v ${command} >/dev/null 2>&1`, { stdio: 'ignore' });
        return true;
    } catch {
        return false;
    }
}

/**
 * Sucht laufende Stage-2-Prozesse (json-graphql-server + contacts.json).
 * @returns {number[]} Liste mit PIDs
 */
function findStage2ProcessPids() {
    const pids = new Set();

    if (hasCommand('lsof')) {
        try {
            const out = execSync(`lsof -ti:${PORT}`, { encoding: 'utf8' });
            out.split('\n')
                .map(s => s.trim())
                .filter(Boolean)
                .map(s => parseInt(s, 10))
                .filter(n => !Number.isNaN(n))
                .forEach(pid => pids.add(pid));
        } catch {
            // ignore
        }
    }

    if (fs.existsSync('/proc')) {
        for (let i = 1; i < 65535; i++) {
            try {
                const cmdline = fs.readFileSync(`/proc/${i}/cmdline`, 'utf8').replace(/\0/g, ' ');
                if (cmdline.includes('json-graphql-server') && cmdline.includes('contacts.json')) {
                    pids.add(i);
                }
            } catch {
                // ignore
            }
        }
    }

    return [...pids];
}

/**
 * Beendet die angegebenen Prozesse mit SIGTERM.
 * @param {number[]} pids - Zu beendende Prozess-IDs
 */
function killProcesses(pids) {
    console.log(`\n[Stage 2] Beende alte Stage-2-Prozesse: ${pids.join(', ')}`);
    pids.forEach(pid => {
        try {
            process.kill(pid, 'SIGTERM');
        } catch (e) {
            console.log(`  Hinweis: PID ${pid} konnte nicht beendet werden (${e.message})`);
        }
    });

    try {
        execSync('sleep 0.4');
    } catch {
        // ignore
    }
}

/**
 * Startet den json-graphql-server mit konfigurierten Host/Port.
 */
function startServer() {
    console.log(`\n[Stage 2] Starte json-graphql-server auf http://${HOST}:${PORT}/`);
    console.log(`[Stage 2] Im Browser (Port-Forwarding): http://localhost:${PORT}/\n`);

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
    const portInUse = await isPortInUse(PORT);

    if (portInUse) {
        const pids = findStage2ProcessPids();

        if (pids.length === 0) {
            console.log(`\n[Stage 2] Port ${PORT} ist belegt, aber kein Stage-2-Restprozess wurde erkannt.`);
            console.log('[Stage 2] Bitte den belegenden Prozess manuell beenden und erneut starten.\n');
            process.exit(1);
        }

        killProcesses(pids);

        if (await isPortInUse(PORT)) {
            console.log(`\n[Stage 2] Port ${PORT} bleibt belegt. Abbruch ohne Crash.`);
            console.log('[Stage 2] Bitte belegenden Prozess manuell prüfen und erneut starten.\n');
            process.exit(1);
        }
    }

    startServer();
})().catch(err => {
    console.error('[Stage 2] Fehler:', err.message);
    process.exit(1);
});

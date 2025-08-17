(function collectDraftData() {
    function collectData() {
        const currentUrl = window.location.href;
        let client = "";
        let round = "";
        let pick = "";

        if (currentUrl.includes("sleeper")) {
            client = "Sleeper"
        } else if (currentUrl.includes("yahoo")) {
            client = "Yahoo"
        } else {
            Error("Unknown fantasy site.")
        }

        // Load existing drafted players from localStorage
        const chosenPlayers = new Set(
            JSON.parse(sessionStorage.getItem('drafted_players') || '[]')
        );

        function saveDraftedPlayers() {
            sessionStorage.setItem('drafted_players', JSON.stringify(Array.from(chosenPlayers)));
        }

        function extractDraftInfo() {
            const newPicks = [];

            if (client === "Yahoo"){
                // DraftResultsTable method
                const tableRows = document.querySelectorAll('.DraftResultsTable .TableBase-bodyTr');
                tableRows.forEach(row => {
                    const teamCell = row.querySelector('.DraftResultsTable-team');
                    const playerCell = row.querySelector('.DraftResultsTable-player');
                    const playerName = playerCell?.textContent.trim();

                    if (teamCell && playerCell && playerName && !chosenPlayers.has(playerName)) {
                        chosenPlayers.add(playerName);
                        newPicks.push({
                            team: teamCell.textContent.trim(),
                            player: playerName,
                            source: client
                        });
                    }
                });

                // <td class="ys-player"> method
                const playerCells = document.querySelectorAll('td.ys-player');
                playerCells.forEach(td => {
                    const name = td.childNodes[0]?.textContent.trim() + ' ' + td.childNodes[2]?.textContent.trim();
                    const team = td.querySelector('abbr')?.textContent.trim();

                    if (name && !chosenPlayers.has(name)) {
                        chosenPlayers.add(name);
                        newPicks.push({
                            player: name,
                            team: team || null,
                            source: client
                        });
                    }
                    // <td data-id="32723" class="ys-player">Jalen Hurts<span class="Dimmed Fz(12px) Fw(500) Whs-nw Mstart-4"><abbr title="Philadelphia Eagles">Phi</abbr><abbr class="Mstart-4" title="Quarterback">- QB</abbr></span></td>
                });



                round = document.querySelector('.DraftBoardHeader-round')?.textContent.trim();
                pick = document.querySelector('.DraftBoardHeader-pick')?.textContent.trim();

            } else if (client === "Sleeper") {
                // 2. Sleeper
                const sleeperCells = document.querySelectorAll('div.cell-container');
                sleeperCells.forEach(div => {
                    const name = div.querySelector('.player-name')?.textContent.trim();
                    const team = div.querySelector('.position')?.textContent.trim();
                    console.log(name)
                    console.log(team)

                    if (name && !chosenPlayers.has(name)) {
                        chosenPlayers.add(name);
                        newPicks.push({
                            player: name,
                            team: team || null,
                            source: client
                        });
                    }
                });

                const info = document.querySelector('.cell.current-pick.is-active .pick')?.textContent.trim().split(".");
                round = info[0];
                pick = info[1];

            }
            

            // Save updated list after any new picks
            var update = false
            if (newPicks.length > 0) {
                saveDraftedPlayers();
                update = true
            }

            return {
                round,
                pick,
                newPicks,
                update,
                allDraftedPlayers: Array.from(chosenPlayers)
            };
        }

        function poll() {
            try {
                const currentData = extractDraftInfo();
                if (currentData['update']) {
                    console.log("📊 Draft Update:", chosenPlayers);
                    // Send these players to my backend
                    const response = fetch("http://localhost:8089", {
                        method: "POST",
                        body: JSON.stringify(currentData)
                    });
                    console.log("Socket Response:", response);
                }
            } catch (e) {
                console.warn("❌ Failed to extract draft info", e);
            }

            requestAnimationFrame(poll); // Continuous polling loop
        }

        poll();
    }
    
    if (!window.hasRunFantasyExtension) {
        window.hasRunFantasyExtension = true;
        
        collectData()
    }
})();

window.onload = function() {
    sessionStorage.setItem('drafted_players', JSON.stringify(Array.from([])));
}
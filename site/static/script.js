document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const runButton = document.getElementById('run-btn');
    const commandInput = document.getElementById('command-input');
    const terminalOutput = document.getElementById('terminal-output');
    const commandButtons = document.querySelectorAll('.command-btn');
    
    // Ensure these elements exist before using them
    const playerListContainer = document.querySelector('#player-list-container');
    const playerCountElement = document.querySelector('#player-count');
    

    // Get the access code from localStorage (if it exists)
    let accessCode = localStorage.getItem('access_code') || '';

    // Function to auto-scroll terminal to the bottom
    function autoScrollTerminal() {
        // Scroll to the bottom of the terminal output
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }

    // Function to add output to terminal with auto-scrolling
    function addToTerminal(content, isError = false) {
        // Create a new div for the output
        const outputDiv = document.createElement('div');
        
        // Add error class if it's an error message
        if (isError) {
            outputDiv.classList.add('error-output');
        }
        
        // Set the content of the div
        outputDiv.innerHTML = content;
        
        // Append to terminal output
        terminalOutput.appendChild(outputDiv);
        
        // Auto-scroll
        autoScrollTerminal();
    }

    // Function to fetch and update player list
    async function updatePlayerList() {
        // Check if elements exist and access code is present
        if (!playerListContainer || !playerCountElement || !accessCode) {
            console.log('Player list elements not found or no access code');
            return;
        }

        try {
            const response = await fetch('/get_players', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ access_code: accessCode })
            });

            const result = await response.json();

            if (result.players) {
                // Update player count
                playerCountElement.textContent = `Players: ${result.total_players || 0}/${result.max_players || 0}`;

                // Clear existing player list
                playerListContainer.innerHTML = '';

                // Add player buttons
                result.players.forEach(player => {
                    const playerButton = document.createElement('button');
                    playerButton.textContent = player;
                    playerButton.classList.add('player-button');
                    playerButton.addEventListener('click', () => {
                        commandInput.value = player;
                    });
                    playerListContainer.appendChild(playerButton);
                });
            }
        } catch (error) {
            console.error('Error updating player list:', error);
        }
    }

    // Only start updating player list if on dashboard
    if (playerListContainer && playerCountElement) {
        // Initial player list update
        updatePlayerList();

        // Update player list every 15 seconds
        const playerListInterval = setInterval(updatePlayerList, 15000);

        // Optional: Clear interval if needed (e.g., on logout)
        function stopPlayerListUpdate() {
            clearInterval(playerListInterval);
        }
    }
    

    // Login functionality
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.json();
                if (result.access_code) {
                    accessCode = result.access_code;
                    localStorage.setItem('access_code', accessCode);
                    localStorage.setItem('username', result.username);  // Add this line
                    window.location.href = '/dashboard';
                } else {
                    alert('Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
            }
        });
    }
    
    // Add Enter key support for command execution
    if (commandInput && runButton) {
        commandInput.addEventListener('keypress', (e) => {
            // Check if the pressed key is Enter
            if (e.key === 'Enter') {
                // Trigger the run button click
                runButton.click();
            }
        });
    }
    
    // Command execution
    if (runButton) {
        runButton.addEventListener('click', async () => {
            const command = commandInput.value;

            console.log('Access Code:', accessCode);  // Log the access code

            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ access_code: accessCode, command })
                });

                const result = await response.json();
                if (response.ok) {
                    // Add command and output to terminal with auto-scrolling
                    addToTerminal(`<strong>Command:</strong> ${command}`);
                    addToTerminal(`<strong>Output:</strong> ${result.output}`);
                } else {
                    // Add error message to terminal
                    addToTerminal(`<strong>Error:</strong> ${result.msg}`, true);
                }
            } catch (error) {
                console.error('Execution error:', error);
                addToTerminal(`<strong>Error:</strong> An error occurred while executing the command.`, true);
            }

            // Clear the command input after execution
            commandInput.value = '';
        });
    }

    // Command button functionality
    commandButtons.forEach(button => {
        button.addEventListener('click', () => {
            const command = button.getAttribute('data-command');
            commandInput.value = command;  // Set the command input to the button's command
        });
    });

    // Add username display and logout functionality
    const usernameDisplay = document.getElementById('username-display');
    const logoutButton = document.getElementById('logout-btn');

    // Set username from localStorage or keep default
    if (usernameDisplay) {
        const username = localStorage.getItem('username') || 'User';
        usernameDisplay.textContent = username;
    }

    // Logout functionality
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            try {
                // Send logout request to server
                const response = await fetch('/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ access_code: accessCode })
                });

                const result = await response.json();

                if (result.success) {
                    // Clear localStorage
                    localStorage.removeItem('access_code');
                    localStorage.removeItem('username');

                    // Redirect to login page
                    window.location.href = '/';
                } else {
                    console.error('Logout failed');
                }
            } catch (error) {
                console.error('Logout error:', error);
            }
        });
    }
});
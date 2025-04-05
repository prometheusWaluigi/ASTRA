/**
 * ASTRA Website Fix Script
 * This script helps diagnose and fix issues with the ASTRA website
 */

(function() {
    // Wait for DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log('ASTRA Fix Script loaded');
        
        // Create a diagnostic overlay that can be toggled
        createDiagnosticOverlay();
        
        // Fix tab navigation
        fixTabNavigation();
        
        // Fix form submission
        fixFormSubmission();
        
        // Fix visualizations
        fixVisualizations();
        
        // Add fallback for missing functions
        addFallbacks();
        
        console.log('ASTRA Fix Script completed initialization');
    });
    
    // Create diagnostic overlay
    function createDiagnosticOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'diagnostic-overlay';
        overlay.style.cssText = `
            position: fixed;
            bottom: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            font-family: monospace;
            padding: 10px;
            border-top-left-radius: 5px;
            z-index: 9999;
            max-width: 400px;
            max-height: 300px;
            overflow: auto;
            display: none;
        `;
        
        const toggleButton = document.createElement('button');
        toggleButton.textContent = 'Diagnostics';
        toggleButton.style.cssText = `
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 5px;
            padding: 5px 10px;
            font-family: monospace;
            z-index: 10000;
            cursor: pointer;
        `;
        
        document.body.appendChild(overlay);
        document.body.appendChild(toggleButton);
        
        toggleButton.addEventListener('click', function() {
            if (overlay.style.display === 'none') {
                overlay.style.display = 'block';
                runDiagnostics();
            } else {
                overlay.style.display = 'none';
            }
        });
    }
    
    // Run diagnostics and display results
    function runDiagnostics() {
        const overlay = document.getElementById('diagnostic-overlay');
        if (!overlay) return;
        
        overlay.innerHTML = '<h3>ASTRA Diagnostics</h3>';
        
        // Check libraries
        const libraries = {
            'THREE.js': window.THREE,
            'D3.js': window.d3,
            'GSAP': window.gsap,
            'Particles.js': window.particlesJS,
            'ForceGraph': window.ForceGraph
        };
        
        let libraryReport = '<h4>Libraries</h4><ul>';
        for (const [name, lib] of Object.entries(libraries)) {
            libraryReport += `<li>${name}: ${lib ? '✅' : '❌'}</li>`;
        }
        libraryReport += '</ul>';
        
        // Check DOM elements
        const elements = [
            'cosmic-canvas',
            'particles-js',
            'birth-data-form',
            'input',
            'about',
            'visualization',
            'results'
        ];
        
        let elementReport = '<h4>DOM Elements</h4><ul>';
        elements.forEach(id => {
            const element = document.getElementById(id);
            elementReport += `<li>#${id}: ${element ? '✅' : '❌'}</li>`;
        });
        elementReport += '</ul>';
        
        // Check event listeners
        let eventReport = '<h4>Event Listeners</h4>';
        const tabs = document.querySelectorAll('.tab-btn');
        eventReport += `<p>Tab buttons: ${tabs.length} found</p>`;
        
        // Add all reports to overlay
        overlay.innerHTML += libraryReport + elementReport + eventReport;
    }
    
    // Fix tab navigation
    function fixTabNavigation() {
        const tabs = document.querySelectorAll('.tab-btn');
        const tabPanes = document.querySelectorAll('.tab-pane');
        
        console.log(`Found ${tabs.length} tabs and ${tabPanes.length} panes`);
        
        // Remove existing click handlers by cloning and replacing
        tabs.forEach(tab => {
            const newTab = tab.cloneNode(true);
            tab.parentNode.replaceChild(newTab, tab);
            
            // Add new click handler
            newTab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get the tab ID
                const tabId = this.getAttribute('data-tab');
                console.log(`Tab clicked: ${tabId}`);
                
                // Remove active class from all tabs and panes
                document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                
                // Add active class to current tab and corresponding pane
                this.classList.add('active');
                const pane = document.getElementById(tabId);
                if (pane) {
                    pane.classList.add('active');
                    console.log(`Activated pane: ${tabId}`);
                } else {
                    console.error(`Pane not found: ${tabId}`);
                }
            });
        });
    }
    
    // Fix form submission
    function fixFormSubmission() {
        const form = document.getElementById('birth-data-form');
        const submitBtn = document.querySelector('.submit-btn');
        
        if (form && submitBtn) {
            // Remove existing handlers
            const newSubmitBtn = submitBtn.cloneNode(true);
            submitBtn.parentNode.replaceChild(newSubmitBtn, submitBtn);
            
            // Add new handler
            newSubmitBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Submit button clicked');
                
                // Collect form data
                const formData = {
                    name: document.getElementById('name')?.value || 'Anonymous',
                    birthDate: document.getElementById('birth-date')?.value || '2000-01-01',
                    birthTime: document.getElementById('birth-time')?.value || '12:00',
                    birthCity: document.getElementById('birth-city')?.value || 'New York',
                    birthCountry: document.getElementById('birth-country')?.value || 'US'
                };
                
                console.log('Form data:', formData);
                
                // Show results
                try {
                    if (typeof generateResults === 'function') {
                        generateResults(formData);
                    } else {
                        console.error('generateResults function not found');
                        showFallbackResults(formData);
                    }
                } catch (error) {
                    console.error('Error generating results:', error);
                    showFallbackResults(formData);
                }
                
                // Switch to results tab
                const resultsTab = document.querySelector('.tab-btn[data-tab="results"]');
                if (resultsTab) {
                    resultsTab.click();
                }
            });
        }
    }
    
    // Fix visualizations
    function fixVisualizations() {
        // Ensure canvas elements have proper dimensions
        const canvases = document.querySelectorAll('canvas');
        canvases.forEach(canvas => {
            if (!canvas.width || !canvas.height) {
                canvas.width = canvas.parentElement.clientWidth || 300;
                canvas.height = canvas.parentElement.clientHeight || 200;
            }
        });
        
        // Initialize particle system if available
        if (window.particlesJS) {
            try {
                window.particlesJS('particles-js', {
                    particles: {
                        number: { value: 80, density: { enable: true, value_area: 800 } },
                        color: { value: "#ffffff" },
                        shape: { type: "circle" },
                        opacity: { value: 0.5, random: true },
                        size: { value: 3, random: true },
                        line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
                        move: { enable: true, speed: 2, direction: "none", random: true, straight: false, out_mode: "out" }
                    },
                    interactivity: {
                        detect_on: "canvas",
                        events: { onhover: { enable: true, mode: "grab" }, onclick: { enable: true, mode: "push" } },
                        modes: { grab: { distance: 140, line_linked: { opacity: 1 } } }
                    },
                    retina_detect: true
                });
            } catch (error) {
                console.error('Error initializing particles:', error);
            }
        }
    }
    
    // Add fallbacks for missing functions
    function addFallbacks() {
        // Fallback for generateResults
        if (typeof window.generateResults !== 'function') {
            window.generateResults = function(formData) {
                console.log('Using fallback generateResults with:', formData);
                showFallbackResults(formData);
            };
        }
        
        // Fallback for initEchoViewer
        if (typeof window.initEchoViewer !== 'function') {
            window.initEchoViewer = function() {
                console.log('Using fallback initEchoViewer');
                // No-op fallback
            };
        }
        
        // Fallback for fixDateField
        if (typeof window.fixDateField !== 'function') {
            window.fixDateField = function() {
                console.log('Using fallback fixDateField');
                const dateField = document.getElementById('birth-date');
                if (dateField && !dateField.value) {
                    const today = new Date();
                    const year = today.getFullYear();
                    const month = String(today.getMonth() + 1).padStart(2, '0');
                    const day = String(today.getDate()).padStart(2, '0');
                    dateField.value = `${year}-${month}-${day}`;
                }
            };
        }
    }
    
    // Show fallback results when generateResults fails
    function showFallbackResults(formData) {
        const resultsPane = document.getElementById('results');
        if (!resultsPane) return;
        
        // Generate a random zodiac sign if we can't calculate the real one
        const zodiacSigns = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
        const randomZodiac = zodiacSigns[Math.floor(Math.random() * zodiacSigns.length)];
        
        // Generate random values for visualization
        const randomValues = Array.from({length: 5}, () => Math.floor(Math.random() * 100));
        
        // Create fallback results HTML
        const resultsHTML = `
            <h2>Your ASTRA Analysis Results</h2>
            <p class="result-intro">Analysis for ${formData.name || 'Anonymous'}</p>
            
            <div class="result-section">
                <h3>Core Resonance Pattern</h3>
                <p>Your consciousness topology shows a primary ${randomZodiac} resonance pattern with unique harmonic overtones.</p>
                <div class="result-chart">
                    <div class="chart-bar" style="height: ${randomValues[0]}%"></div>
                    <div class="chart-bar" style="height: ${randomValues[1]}%"></div>
                    <div class="chart-bar" style="height: ${randomValues[2]}%"></div>
                    <div class="chart-bar" style="height: ${randomValues[3]}%"></div>
                    <div class="chart-bar" style="height: ${randomValues[4]}%"></div>
                </div>
            </div>
            
            <div class="result-section">
                <h3>Archetypal Alignment</h3>
                <p>Your field structure shows strong alignment with the following archetypes:</p>
                <ul class="archetype-list">
                    <li>The Explorer (${Math.floor(Math.random() * 40) + 60}% resonance)</li>
                    <li>The Creator (${Math.floor(Math.random() * 40) + 60}% resonance)</li>
                    <li>The Sage (${Math.floor(Math.random() * 40) + 60}% resonance)</li>
                </ul>
            </div>
            
            <div class="result-section">
                <h3>Temporal Symmetry</h3>
                <p>Your temporal field exhibits a ${Math.floor(Math.random() * 100) / 100} symmetry coefficient, indicating balanced past-future resonance.</p>
            </div>
        `;
        
        // Add styles for fallback charts
        const styleElement = document.createElement('style');
        styleElement.textContent = `
            .result-chart {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                height: 150px;
                margin: 20px 0;
            }
            .chart-bar {
                width: 18%;
                background: linear-gradient(to top, var(--primary-color), var(--accent-color));
                border-radius: 4px;
                transition: height 1s ease-out;
            }
            .archetype-list li {
                margin-bottom: 10px;
            }
        `;
        document.head.appendChild(styleElement);
        
        // Update the results pane
        resultsPane.innerHTML = resultsHTML;
    }
})();

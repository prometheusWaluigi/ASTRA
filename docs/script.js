// ASTRA Web Interface JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button and corresponding pane
            button.classList.add('active');
            const tabId = button.dataset.tab;
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Form submission
    const birthForm = document.getElementById('birth-data-form');
    birthForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading spinner
        document.getElementById('loading').classList.remove('hidden');
        
        // Collect form data
        const formData = {
            name: document.getElementById('name').value,
            birthDate: document.getElementById('birth-date').value,
            birthTime: document.getElementById('birth-time').value,
            birthCity: document.getElementById('birth-city').value,
            birthCountry: document.getElementById('birth-country').value
        };
        
        // Simulate API call with timeout
        setTimeout(() => {
            generateMockResults(formData);
            document.getElementById('loading').classList.add('hidden');
            
            // Switch to visualization tab
            document.querySelector('[data-tab="visualization"]').click();
            
            // After 2 seconds, show the results tab
            setTimeout(() => {
                document.querySelector('[data-tab="results"]').click();
            }, 2000);
        }, 3000);
    });
    
    // Function to generate mock results
    function generateMockResults(formData) {
        // Parse date components
        const birthDate = new Date(formData.birthDate + 'T' + formData.birthTime);
        const year = birthDate.getFullYear();
        const month = birthDate.getMonth() + 1;
        const day = birthDate.getDate();
        const hour = birthDate.getHours();
        const minute = birthDate.getMinutes();
        
        // Generate mock natal report
        const natalReport = document.querySelector('#natal-report .report-content');
        natalReport.innerHTML = `
            <div class="report-item">
                <p><strong>Name:</strong> ${formData.name}</p>
                <p><strong>Birth Date:</strong> ${month}/${day}/${year}</p>
                <p><strong>Birth Time:</strong> ${hour}:${minute.toString().padStart(2, '0')}</p>
                <p><strong>Location:</strong> ${formData.birthCity}, ${formData.birthCountry}</p>
            </div>
            <div class="report-item">
                <h4>Planetary Positions</h4>
                <ul>
                    <li>☉ Sun: ${getZodiacSign(month, day)} ${getRandomDegree()}°</li>
                    <li>☽ Moon: ${getRandomZodiacSign()} ${getRandomDegree()}°</li>
                    <li>☿ Mercury: ${getRandomZodiacSign()} ${getRandomDegree()}°</li>
                    <li>♀ Venus: ${getRandomZodiacSign()} ${getRandomDegree()}°</li>
                    <li>♂ Mars: ${getRandomZodiacSign()} ${getRandomDegree()}°</li>
                    <li>♃ Jupiter: ${getRandomZodiacSign()} ${getRandomDegree()}°</li>
                    <li>♄ Saturn: ${getRandomZodiacSign()} ${getRandomDegree()}°</li>
                </ul>
            </div>
        `;
        document.getElementById('natal-report').classList.remove('hidden');
        
        // Generate mock field analysis
        const fieldAnalysis = document.querySelector('#field-analysis .report-content');
        fieldAnalysis.innerHTML = `
            <div class="report-item">
                <p>QualiaField initialized from birth chart data with grid size 128x128.</p>
                <p>Field evolution complete using fKPZχ equation with parameters:</p>
                <ul>
                    <li>α (alpha): ${(Math.random() * 0.5 + 0.3).toFixed(2)}</li>
                    <li>β (beta): ${(Math.random() * 0.6 + 0.7).toFixed(2)}</li>
                    <li>γ (gamma): ${(Math.random() * 0.4 - 0.2).toFixed(2)}</li>
                    <li>η (eta): ${(Math.random() * 0.1 + 0.05).toFixed(2)}</li>
                </ul>
                <p>Evolution duration: 2.0 time units with dt=0.01</p>
            </div>
        `;
        document.getElementById('field-analysis').classList.remove('hidden');
        
        // Generate mock topology analysis
        const topoAnalysis = document.querySelector('#topology-analysis .report-content');
        const betti0 = Math.floor(Math.random() * 5) + 1;
        const betti1 = Math.floor(Math.random() * 3);
        const betti2 = Math.floor(Math.random() * 2);
        
        topoAnalysis.innerHTML = `
            <div class="report-item">
                <p>Topological analysis complete using persistent homology.</p>
                <h4>Betti Numbers</h4>
                <p>β₀ = ${betti0} (connected components)</p>
                <p>β₁ = ${betti1} (loops/cycles)</p>
                <p>β₂ = ${betti2} (voids/cavities)</p>
                
                <h4>Ricci Curvature Analysis</h4>
                <p>Average Ollivier-Ricci curvature: ${(Math.random() * 0.4 - 0.2).toFixed(3)}</p>
                <p>Curvature distribution: ${Math.random() > 0.5 ? 'Predominantly negative' : 'Predominantly positive'}</p>
                <p>This indicates a ${Math.random() > 0.5 ? 'hyperbolic' : 'elliptic'} psychological space.</p>
            </div>
        `;
        document.getElementById('topology-analysis').classList.remove('hidden');
        
        // Generate mock narrative events
        const narrativeEvents = document.querySelector('#narrative-events .report-content');
        const events = generateRandomEvents();
        let eventsHTML = `<div class="report-item"><h4>Detected Archetypal Events</h4><ul>`;
        
        events.forEach(event => {
            eventsHTML += `<li><strong>${event.type}:</strong> ${event.description}</li>`;
        });
        
        eventsHTML += `</ul></div>`;
        narrativeEvents.innerHTML = eventsHTML;
        document.getElementById('narrative-events').classList.remove('hidden');
        
        // Update visualizations
        updateVisualizations(formData);
    }
    
    // Function to update visualizations
    function updateVisualizations(formData) {
        // Generate random field images
        const initialField = document.getElementById('initial-field');
        const evolvedField = document.getElementById('evolved-field');
        const topologyVis = document.getElementById('topology-vis');
        
        // Replace placeholders with mock visualizations
        initialField.innerHTML = `
            <h3>Initial QualiaField χ(x,0)</h3>
            <img src="https://raw.githubusercontent.com/prometheusWaluigi/ASTRA/main/output/diagnostic/initial_field.png" 
                 alt="Initial QualiaField" class="field-image">
            <p>Birth configuration at t=0</p>
        `;
        
        evolvedField.innerHTML = `
            <h3>Evolved QualiaField χ(x,t)</h3>
            <img src="https://raw.githubusercontent.com/prometheusWaluigi/ASTRA/main/output/diagnostic/evolved_state.png" 
                 alt="Evolved QualiaField" class="field-image">
            <p>Field after evolution (t=2.0)</p>
        `;
        
        topologyVis.innerHTML = `
            <h3>Topological Analysis</h3>
            <img src="https://raw.githubusercontent.com/prometheusWaluigi/ASTRA/main/output/diagnostic/field_graph.png" 
                 alt="Field Topology" class="field-image">
            <p>Graph representation of field topology</p>
        `;
    }
    
    // Helper functions for mock data
    function getZodiacSign(month, day) {
        const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
        
        // Simple algorithm to determine zodiac sign based on month and day
        if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) return signs[0]; // Aries
        if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) return signs[1]; // Taurus
        if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) return signs[2]; // Gemini
        if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) return signs[3]; // Cancer
        if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) return signs[4]; // Leo
        if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) return signs[5]; // Virgo
        if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) return signs[6]; // Libra
        if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) return signs[7]; // Scorpio
        if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) return signs[8]; // Sagittarius
        if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) return signs[9]; // Capricorn
        if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) return signs[10]; // Aquarius
        return signs[11]; // Pisces
    }
    
    function getRandomZodiacSign() {
        const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
        return signs[Math.floor(Math.random() * signs.length)];
    }
    
    function getRandomDegree() {
        return Math.floor(Math.random() * 30);
    }
    
    function generateRandomEvents() {
        const eventTypes = [
            { type: "EMERGENCE", descriptions: [
                "Manifestation of creative potential in the first quadrant",
                "Rising consciousness pattern in the Jupiter sector",
                "Self-organizing structure forming near the Venus harmonic",
                "Novel attractor state emerging from chaos region"
            ]},
            { type: "DISSOLUTION", descriptions: [
                "Breakdown of rigid structures in the Saturn domain",
                "Destabilization of fixed patterns in the Mars sector",
                "Phase transition from ordered to chaotic state",
                "Boundary dissolution between ego and environment"
            ]},
            { type: "RECURSION", descriptions: [
                "Self-referential loop detected in the Mercury sector",
                "Fractal pattern with increasing complexity in the Pluto domain",
                "Nested information structure with high Kolmogorov complexity",
                "Feedback loop between conscious and unconscious processes"
            ]},
            { type: "BIFURCATION", descriptions: [
                "Critical decision point with diverging trajectories",
                "Symmetry breaking in the primary attractor basin",
                "Transition from single to multiple equilibria states",
                "Nucleation of competing stability zones"
            ]},
            { type: "RESONANCE", descriptions: [
                "Strong harmonic coupling between Moon and Neptune sectors",
                "Phase synchronization across multiple field domains",
                "Cross-frequency coupling between alpha and gamma processes",
                "Constructive interference pattern in the Venus-Jupiter axis"
            ]}
        ];
        
        // Generate 2-4 random events
        const numEvents = Math.floor(Math.random() * 3) + 2;
        let events = [];
        
        for (let i = 0; i < numEvents; i++) {
            const eventType = eventTypes[Math.floor(Math.random() * eventTypes.length)];
            const description = eventType.descriptions[Math.floor(Math.random() * eventType.descriptions.length)];
            
            events.push({
                type: eventType.type,
                description: description
            });
        }
        
        return events;
    }
});

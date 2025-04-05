// ASTRA Web Interface - Advanced JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cosmic background
    initCosmicBackground();
    
    // Tab functionality
    initTabs();
    
    // Form submission
    initForm();
    
    // Add cosmic animations
    addCosmicAnimations();
});

// ======== COSMIC BACKGROUND EFFECT ========
function initCosmicBackground() {
    // Create floating stars/particles
    createCosmicParticles();
    
    // Add pulsing glow effects
    const glowElements = document.querySelectorAll('.logo-glow, .placeholder-glow');
    glowElements.forEach(element => {
        setInterval(() => {
            element.style.opacity = 0.1 + Math.random() * 0.3;
            element.style.filter = `blur(${15 + Math.random() * 10}px)`;
        }, 2000);
    });
}

function createCosmicParticles() {
    const container = document.getElementById('cosmic-canvas');
    if (!container) return;
    
    // Create stars
    for (let i = 0; i < 200; i++) {
        const star = document.createElement('div');
        star.className = 'cosmic-particle';
        
        // Random size
        const size = Math.random() * 3 + 1;
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Random color
        const colors = ['#8a2be2', '#0096ff', '#ff3e9d', '#ffffff'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        // Set styles
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${posX}%`;
        star.style.top = `${posY}%`;
        star.style.backgroundColor = color;
        star.style.opacity = Math.random() * 0.7 + 0.3;
        
        // Animation duration
        const animDuration = Math.random() * 50 + 20;
        star.style.animation = `twinkle ${animDuration}s infinite`;
        
        // Add to container
        container.appendChild(star);
    }
    
    // Add cosmic orbs
    for (let i = 0; i < 5; i++) {
        const orb = document.createElement('div');
        orb.className = 'cosmic-orb';
        
        // Random size
        const size = Math.random() * 200 + 100;
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Set styles
        orb.style.width = `${size}px`;
        orb.style.height = `${size}px`;
        orb.style.left = `${posX}%`;
        orb.style.top = `${posY}%`;
        
        // Add to container
        container.appendChild(orb);
    }
}

// ======== TAB NAVIGATION ========
function initTabs() {
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
}

// ======== FORM HANDLING ========
function initForm() {
    const birthForm = document.getElementById('birth-data-form');
    const nameInput = document.getElementById('name');
    const birthCityInput = document.getElementById('birth-city');
    const birthCountrySelect = document.getElementById('birth-country');
    
    // Set up input validation
    nameInput.addEventListener('input', validateName);
    birthCityInput.addEventListener('input', validateCity);
    birthCountrySelect.addEventListener('change', function() {
        // Clear city input when country changes
        birthCityInput.value = '';
        // Remove validation classes
        birthCityInput.classList.remove('valid', 'invalid');
    });
    
    // Create datalist for city autocomplete
    setupCityAutocomplete();
    
    birthForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all inputs before submission
        const isNameValid = validateName();
        const isCityValid = validateCity();
        const isCountryValid = birthCountrySelect.value !== '';
        const isBirthDateValid = document.getElementById('birth-date').value !== '';
        const isBirthTimeValid = document.getElementById('birth-time').value !== '';
        
        // Check if all inputs are valid
        if (!isNameValid || !isCityValid || !isCountryValid || !isBirthDateValid || !isBirthTimeValid) {
            // Show validation errors
            if (!isNameValid) nameInput.classList.add('invalid');
            if (!isCityValid) birthCityInput.classList.add('invalid');
            if (!isCountryValid) birthCountrySelect.classList.add('invalid');
            if (!isBirthDateValid) document.getElementById('birth-date').classList.add('invalid');
            if (!isBirthTimeValid) document.getElementById('birth-time').classList.add('invalid');
            
            // Shake the form to indicate error
            birthForm.classList.add('shake');
            setTimeout(() => birthForm.classList.remove('shake'), 500);
            
            return; // Don't submit if validation fails
        }
        
        // Show loading spinner
        document.getElementById('loading').classList.remove('hidden');
        
        // Collect form data
        const formData = {
            name: nameInput.value,
            birthDate: document.getElementById('birth-date').value,
            birthTime: document.getElementById('birth-time').value,
            birthCity: birthCityInput.value,
            birthCountry: birthCountrySelect.value
        };
        
        // Simulate API call with timeout
        setTimeout(() => {
            generateResults(formData);
            document.getElementById('loading').classList.add('hidden');
            
            // Switch to visualization tab
            document.querySelector('[data-tab="visualization"]').click();
            
            // After 2 seconds, show the results tab
            setTimeout(() => {
                document.querySelector('[data-tab="results"]').click();
            }, 2000);
        }, 3000);
    });
}

// Validate name input
function validateName() {
    const nameInput = document.getElementById('name');
    const name = nameInput.value.trim();
    
    // Name should be at least 2 characters long and contain only letters and spaces
    const isValid = name.length >= 2 && /^[A-Za-z\s'-]+$/.test(name);
    
    // Update input styling based on validation
    if (name === '') {
        nameInput.classList.remove('valid', 'invalid');
    } else {
        nameInput.classList.toggle('valid', isValid);
        nameInput.classList.toggle('invalid', !isValid);
    }
    
    return isValid;
}

// Validate city input
function validateCity() {
    const cityInput = document.getElementById('birth-city');
    const countrySelect = document.getElementById('birth-country');
    const city = cityInput.value.trim();
    const country = countrySelect.value;
    
    // If no country is selected, we can't validate the city
    if (country === '') {
        cityInput.classList.remove('valid', 'invalid');
        return false;
    }
    
    // Check if city exists in the selected country
    const cityExists = isCityInCountry(city, country);
    const isValid = city.length >= 2 && cityExists;
    
    // Update input styling based on validation
    if (city === '') {
        cityInput.classList.remove('valid', 'invalid');
    } else {
        cityInput.classList.toggle('valid', isValid);
        cityInput.classList.toggle('invalid', !isValid);
    }
    
    return isValid;
}

// Setup city autocomplete
function setupCityAutocomplete() {
    const cityInput = document.getElementById('birth-city');
    const countrySelect = document.getElementById('birth-country');
    
    // Create datalist element for city suggestions
    let datalist = document.getElementById('city-suggestions');
    if (!datalist) {
        datalist = document.createElement('datalist');
        datalist.id = 'city-suggestions';
        document.body.appendChild(datalist);
        cityInput.setAttribute('list', 'city-suggestions');
    }
    
    // Update city suggestions when country changes
    countrySelect.addEventListener('change', function() {
        updateCitySuggestions(countrySelect.value);
    });
    
    // Update city suggestions when typing
    cityInput.addEventListener('input', function() {
        const country = countrySelect.value;
        if (country) {
            updateCitySuggestions(country, cityInput.value);
        }
    });
}

// Update city suggestions in datalist
function updateCitySuggestions(country, filter = '') {
    const datalist = document.getElementById('city-suggestions');
    datalist.innerHTML = ''; // Clear previous suggestions
    
    if (!country) return;
    
    // Get cities for the selected country
    const cities = getCitiesForCountry(country);
    
    // Filter cities based on input
    const filteredCities = filter ? 
        cities.filter(city => city.toLowerCase().includes(filter.toLowerCase())) : 
        cities;
    
    // Limit to top 10 suggestions
    const topCities = filteredCities.slice(0, 10);
    
    // Add city options to datalist
    topCities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        datalist.appendChild(option);
    });
}

// Check if a city exists in the selected country
function isCityInCountry(city, country) {
    if (!city || !country) return false;
    
    const cities = getCitiesForCountry(country);
    return cities.some(c => c.toLowerCase() === city.toLowerCase());
}

// Get cities for a country
function getCitiesForCountry(country) {
    // Major cities database
    const cityDatabase = {
        'US': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Indianapolis', 'Charlotte', 'San Francisco', 'Seattle', 'Denver', 'Washington'],
        'CA': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City', 'Hamilton', 'Kitchener'],
        'UK': ['London', 'Birmingham', 'Manchester', 'Glasgow', 'Liverpool', 'Bristol', 'Edinburgh', 'Leeds', 'Sheffield', 'Cardiff'],
        'AU': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra', 'Newcastle', 'Wollongong', 'Hobart'],
        'DE': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Leipzig', 'Dortmund', 'Essen'],
        'FR': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille'],
        'IN': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Ghaziabad'],
        'JP': ['Tokyo', 'Yokohama', 'Osaka', 'Nagoya', 'Sapporo', 'Kobe', 'Kyoto', 'Fukuoka', 'Kawasaki', 'Saitama'],
        'CN': ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen', 'Chongqing', 'Tianjin', 'Wuhan', 'Chengdu', 'Hangzhou', 'Nanjing'],
        'BR': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre'],
        'RU': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan', 'Chelyabinsk', 'Omsk', 'Samara', 'Rostov-on-Don', 'Ufa'],
        'ZA': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth', 'Bloemfontein', 'Pietermaritzburg', 'East London', 'Nelspruit', 'Kimberley'],
        'ES': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza', 'Málaga', 'Murcia', 'Palma', 'Las Palmas', 'Bilbao'],
        'IT': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Catania', 'Bari'],
        'MX': ['Mexico City', 'Ecatepec', 'Guadalajara', 'Puebla', 'Juárez', 'Tijuana', 'León', 'Zapopan', 'Monterrey', 'Nezahualcóyotl']
    };
    
    // Return default cities for countries not in the database
    if (!cityDatabase[country]) {
        return ['Please enter a valid city'];
    }
    
    return cityDatabase[country];
}

// ======== COSMIC ANIMATIONS ========
function addCosmicAnimations() {
    // Glitch text effect
    const glitchText = document.querySelector('.glitch-text');
    if (glitchText) {
        setInterval(() => {
            glitchText.classList.add('glitching');
            setTimeout(() => {
                glitchText.classList.remove('glitching');
            }, 200);
        }, 5000);
    }
    
    // Sparkle animation
    const sparkle = document.querySelector('.sparkle');
    if (sparkle) {
        setInterval(() => {
            sparkle.style.transform = 'scale(1.5)';
            sparkle.style.opacity = '1';
            setTimeout(() => {
                sparkle.style.transform = 'scale(1)';
                sparkle.style.opacity = '0.8';
            }, 500);
        }, 3000);
    }
}
// ======== GENERATE RESULTS ========
function generateResults(formData) {
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
    updateVisualizations();
}

// ======== UPDATE VISUALIZATIONS ========
function updateVisualizations() {
    // Update field visualizations
    const initialField = document.getElementById('initial-field');
    const evolvedField = document.getElementById('evolved-field');
    const topologyVis = document.getElementById('topology-vis');
    
    // Replace placeholders with mock visualizations
    initialField.querySelector('.placeholder-img').style.display = 'none';
    evolvedField.querySelector('.placeholder-img').style.display = 'none';
    topologyVis.querySelector('.placeholder-img').style.display = 'none';
    
    // Show field containers
    initialField.querySelector('.field-container').style.display = 'block';
    evolvedField.querySelector('.field-container').style.display = 'block';
    topologyVis.querySelector('.topology-viz-container').style.display = 'block';
    
    // Betti numbers for display
    const betti0 = Math.floor(Math.random() * 5) + 1;
    const betti1 = Math.floor(Math.random() * 3);
    const betti2 = Math.floor(Math.random() * 2);
    const ricciCurvature = (Math.random() * 0.4 - 0.2).toFixed(3);
    
    // Update statistics display
    document.getElementById('betti0').textContent = betti0;
    document.getElementById('betti1').textContent = betti1;
    document.getElementById('betti2').textContent = betti2;
    document.getElementById('ricci-curvature').textContent = ricciCurvature;
    
    // Initialize canvas visualizations
    initializeCanvasVisualizations();
}

// ======== CANVAS VISUALIZATIONS ========
function initializeCanvasVisualizations() {
    // Initial field visualization
    const initialCanvas = document.getElementById('initial-field-canvas');
    if (initialCanvas) {
        const ctx = initialCanvas.getContext('2d');
        drawFieldVisualization(ctx, initialCanvas.width, initialCanvas.height, 'initial');
    }
    
    // Evolved field visualization
    const evolvedCanvas = document.getElementById('evolved-field-canvas');
    if (evolvedCanvas) {
        const ctx = evolvedCanvas.getContext('2d');
        drawFieldVisualization(ctx, evolvedCanvas.width, evolvedCanvas.height, 'evolved');
    }
    
    // Add event listener for timeline slider
    const timeline = document.getElementById('evolution-timeline');
    if (timeline) {
        timeline.addEventListener('input', function() {
            const ctx = document.getElementById('evolved-field-canvas').getContext('2d');
            const value = parseInt(this.value) / 100; // 0-1 range
            drawFieldVisualization(ctx, evolvedCanvas.width, evolvedCanvas.height, 'evolved', value);
        });
    }
    
    // Topology visualization
    createTopologyGraph();
}
// ======== VISUALIZATION FUNCTIONS ========
function drawFieldVisualization(ctx, width, height, type, timeValue = 0) {
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Set up parameters
    const cellSize = 5;
    const cols = Math.floor(width / cellSize);
    const rows = Math.floor(height / cellSize);
    
    // Different color schemes for initial vs evolved
    const colorScheme = type === 'initial' ? 
        ['#8a2be2', '#9932cc', '#9370db', '#ba55d3', '#da70d6'] : // Purple scheme
        ['#0096ff', '#00bfff', '#00d2ff', '#00e5ff', '#00f7ff'];  // Blue scheme
    
    // Draw field with gradients
    ctx.globalAlpha = 1;
    
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            // Value is based on position and perlin-like noise
            let value = Math.sin(x * 0.05) * Math.cos(y * 0.05) * 0.5 + 0.5;
            
            // For evolved, add time factor
            if (type === 'evolved') {
                value = Math.sin(x * 0.05 + timeValue * 2) * 
                        Math.cos(y * 0.05 + timeValue) * 0.5 + 0.5;
                
                // Add some oscillation
                value += Math.sin(timeValue * 3 + x * 0.02 + y * 0.02) * 0.2;
            }
            
            // Add noise
            value += Math.random() * 0.1 - 0.05;
            value = Math.max(0, Math.min(1, value));
            
            // Get color based on value
            const colorIndex = Math.floor(value * (colorScheme.length - 1));
            ctx.fillStyle = colorScheme[colorIndex];
            
            // Calculate height (for 3D effect)
            const heightFactor = value * 0.8 + 0.2; // 0.2-1.0 range
            
            // Draw cell
            ctx.fillRect(
                x * cellSize, 
                y * cellSize, 
                cellSize * heightFactor, 
                cellSize * heightFactor
            );
        }
    }
    
    // Add some glow effect
    const gradient = ctx.createRadialGradient(
        width/2, height/2, 10,
        width/2, height/2, width/2
    );
    
    const primaryColor = type === 'initial' ? '#8a2be2' : '#0096ff';
    gradient.addColorStop(0, primaryColor + '80'); // 50% opacity
    gradient.addColorStop(1, 'transparent');
    
    ctx.globalAlpha = 0.4;
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
}

function createTopologyGraph() {
    const graphContainer = document.getElementById('topology-3d-graph');
    if (!graphContainer) return;
    
    // Generate nodes and links data for 3D-force-graph
    const nodesData = [];
    const linksData = [];
    
    // Create nodes
    for (let i = 0; i < 30; i++) {
        nodesData.push({
            id: i,
            value: Math.random(),
            betti: Math.floor(Math.random() * 3), // 0, 1, or 2
            curvature: Math.random() * 2 - 1, // -1 to 1
            color: getRandomColor()
        });
    }
    
    // Create links between nodes that are close
    for (let i = 0; i < nodesData.length; i++) {
        // Connect each node to 2-4 others
        const numLinks = Math.floor(Math.random() * 3) + 2;
        
        for (let j = 0; j < numLinks; j++) {
            const target = Math.floor(Math.random() * nodesData.length);
            if (target !== i) {
                linksData.push({
                    source: i,
                    target: target,
                    weight: Math.random() * 0.8 + 0.2 // 0.2 to 1.0
                });
            }
        }
    }
    
    // Create the graph data
    const graphData = {
        nodes: nodesData,
        links: linksData
    };
    
    // Create 3D force graph
    const Graph = ForceGraph3D()
        (graphContainer)
        .backgroundColor('rgba(0,0,0,0)')
        .nodeColor(node => node.color)
        .nodeLabel(node => `Node ${node.id}: Value ${node.value.toFixed(2)}`)
        .linkWidth(link => link.weight * 2)
        .linkColor(() => 'rgba(138, 43, 226, 0.2)')
        .graphData(graphData);
    
    // Store graph reference for visualization toggling
    window.topologyGraph = Graph;
    
    // Visualization toggle
    document.querySelectorAll('.viz-toggle').forEach(btn => {
        btn.addEventListener('click', function() {
            // Update active state
            document.querySelectorAll('.viz-toggle').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Get visualization type
            const vizType = this.dataset.viz;
            
            // Update graph colors based on visualization type
            if (vizType === 'graph') {
                Graph.nodeColor(node => node.color);
            } else if (vizType === 'betti') {
                Graph.nodeColor(node => {
                    return node.betti === 0 ? '#8a2be2' : 
                           node.betti === 1 ? '#0096ff' : '#ff3e9d';
                });
            } else if (vizType === 'curvature') {
                Graph.nodeColor(node => {
                    return node.curvature < 0 ? '#ff3e9d' : 
                           node.curvature === 0 ? '#ffffff' : '#0096ff';
                });
            }
        });
    });
}

// ======== HELPER FUNCTIONS ========
function getZodiacSign(month, day) {
    const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    
    // Simple algorithm to determine zodiac sign
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

function getRandomColor() {
    const colors = [
        '#8a2be2', // Purple
        '#0096ff', // Blue
        '#ff3e9d', // Pink
        '#36e278', // Green
        '#ffaa00'  // Orange
    ];
    return colors[Math.floor(Math.random() * colors.length)];
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
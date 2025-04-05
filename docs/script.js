// ASTRA Web Interface - Advanced JavaScript
document.addEventListener('DOMContentLoaded', function() {
    try {
        // Initialize cosmic background
        initCosmicBackground();
        
        // Configure particle.js
        initializeParticles();
        
        // Tab functionality
        initTabs();
        
        // Form submission
        initForm();
        
        // Add cosmic animations
        addCosmicAnimations();
        
        // Initialize echo viewer
        initEchoViewer();
        
        // Initialize city datalist
        createDatalist();
        setupCityAutocomplete();
        
        // Fix date field with current date
        fixDateField();
        
        // Add responsive handlers
        addResponsiveHandlers();
        
        console.log('ASTRA interface successfully initialized');
    } catch (error) {
        console.error('Error during initialization:', error);
        showErrorMessage('Failed to initialize ASTRA interface. Please refresh the page.');
    }
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
    document.addEventListener('click', function(e) {
        if (e.target.matches('.tab-btn')) {
            const tabId = e.target.dataset.tab;
            const tabPanes = document.querySelectorAll('.tab-pane');
            
            // Single DOM update for all tab buttons
            document.querySelectorAll('.tab-btn').forEach(btn => 
                btn.classList.toggle('active', btn === e.target));
            
            // Single DOM update for tab panes
            tabPanes.forEach(pane => 
                pane.classList.toggle('active', pane.id === tabId));
        }
    });
}

// ======== FORM HANDLING ========
function initForm() {
    const birthForm = document.getElementById('birth-data-form');
    const nameInput = document.getElementById('name');
    const birthCityInput = document.getElementById('birth-city');
    const birthCountrySelect = document.getElementById('birth-country');
    const generateBtn = document.getElementById('generate-btn');
    const formError = document.getElementById('form-error');
    
    if (!birthForm || !nameInput || !birthCityInput || !birthCountrySelect || !generateBtn) {
        console.error('Form elements not found');
        showErrorMessage('Form initialization failed. Please refresh the page.');
        return;
    }
    
    console.log('Initializing form handlers');
    
    // Set up input validation
    nameInput.addEventListener('input', validateName);
    birthCityInput.addEventListener('input', validateCity);
    birthCountrySelect.addEventListener('change', function() {
        // Clear city input when country changes
        birthCityInput.value = '';
        // Remove validation classes
        birthCityInput.classList.remove('valid', 'invalid');
        
        // Update city suggestions for the new country
        updateCitySuggestions(this.value, '');
        
        // Hide error message if it's showing
        hideErrorMessage();
    });
    
    // Create datalist for city autocomplete
    setupCityAutocomplete();
    
    // Add click handler for the generate button
    generateBtn.addEventListener('click', function() {
        try {
            const loadingIndicator = document.getElementById('loading');
            if (!loadingIndicator) {
                throw new Error('Loading indicator not found');
            }
            
            // Validate all inputs before submission
            const isNameValid = validateName();
            const isCityValid = validateCity();
            const isCountryValid = birthCountrySelect.value !== '';
            const isBirthDateValid = validateDateField();
            const isBirthTimeValid = validateTimeField();
            
            // Check if all inputs are valid
            if (!isNameValid || !isCityValid || !isCountryValid || !isBirthDateValid || !isBirthTimeValid) {
                // Show validation errors
                if (!isNameValid) nameInput.classList.add('invalid');
                if (!isCityValid) birthCityInput.classList.add('invalid');
                if (!isCountryValid) birthCountrySelect.classList.add('invalid');
                if (!isBirthDateValid) document.getElementById('birth-date').classList.add('invalid');
                if (!isBirthTimeValid) document.getElementById('birth-time').classList.add('invalid');
                
                // Show error message
                showErrorMessage('Please fill in all required fields correctly.');
                
                // Shake the form to indicate error
                birthForm.classList.add('shake');
                setTimeout(() => birthForm.classList.remove('shake'), 500);
                
                return;
            }
            
            // Hide any previous error messages
            hideErrorMessage();
            
            // Show loading indicator
            loadingIndicator.classList.remove('hidden');
            
            // Collect form data
            const formData = {
                name: nameInput.value,
                birthDate: document.getElementById('birth-date').value,
                birthTime: document.getElementById('birth-time').value,
                birthCity: birthCityInput.value,
                birthCountry: birthCountrySelect.value
            };
            
            console.log('Form data collected:', formData);
            
            // Simulate API call with timeout
            setTimeout(() => {
                try {
                    generateResults(formData);
                    loadingIndicator.classList.add('hidden');
                    
                    // Switch to visualization tab
                    const visualizationTab = document.querySelector('[data-tab="visualization"]');
                    if (visualizationTab) {
                        visualizationTab.click();
                        
                        // After 2 seconds, show the results tab
                        setTimeout(() => {
                            const resultsTab = document.querySelector('[data-tab="results"]');
                            if (resultsTab) {
                                resultsTab.click();
                            }
                        }, 2000);
                    }
                } catch (error) {
                    console.error('Error generating results:', error);
                    loadingIndicator.classList.add('hidden');
                    showErrorMessage('Failed to generate results. Please try again.');
                }
            }, 3000);
        } catch (error) {
            console.error('Error in form submission:', error);
            showErrorMessage('An error occurred. Please try again.');
        }
    });
    
    // Keep the submit handler for backward compatibility
    birthForm.addEventListener('submit', function(e) {
        e.preventDefault();
        generateBtn.click();
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
    
    if (!cityInput || !countrySelect) {
        console.error('City input or country select not found');
        return false;
    }
    
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
    
    console.log(`City validation: ${city} is ${isValid ? 'valid' : 'invalid'} for ${country}`);
    return isValid;
}

// Setup city autocomplete
function setupCityAutocomplete() {
    const cityInput = document.getElementById('birth-city');
    const countrySelect = document.getElementById('birth-country');
    const datalist = document.getElementById('city-suggestions') || createDatalist();

    let timeoutId;
    const updateHandler = () => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            updateCitySuggestions(countrySelect.value, cityInput.value);
        }, 300);
    };

    countrySelect.addEventListener('change', updateHandler, { passive: true });
    cityInput.addEventListener('input', updateHandler, { passive: true });
}

// Update city suggestions in datalist
function updateCitySuggestions(country, filter = '') {
    const datalist = document.getElementById('city-suggestions');
    if (!datalist) {
        console.error('City suggestions datalist not found');
        return;
    }
    
    const cities = getCitiesForCountry(country);
    if (!cities || cities.length === 0) {
        console.log(`No cities found for country: ${country}`);
        return;
    }
    
    const fragment = document.createDocumentFragment();
    
    cities.filter(city => city.toLowerCase().includes(filter.toLowerCase()))
        .slice(0, 10)
        .forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            fragment.appendChild(option);
        });

    requestAnimationFrame(() => {
        datalist.innerHTML = '';
        datalist.appendChild(fragment);
        console.log(`Updated city suggestions for ${country}: ${cities.slice(0, 3).join(', ')}...`);
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
    const domCache = {
        natalReport: document.querySelector('#natal-report .report-content'),
        visualizationCanvases: new Map(),
        topologyGraph: null
    };

    ['initial-field-canvas', 'evolved-field-canvas'].forEach(id => {
        const canvas = document.getElementById(id);
        if (canvas && !domCache.visualizationCanvases.has(id)) {
            domCache.visualizationCanvases.set(id, {
                element: canvas,
                ctx: canvas.getContext('2d')
            });
        }
    });
    
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
    const domCache = {
        natalReport: document.querySelector('#natal-report .report-content'),
        visualizationCanvases: new Map(),
        topologyGraph: Graph
    };
    
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

// This content should already be replaced by now

// Initialize particles.js
function initializeParticles() {
    const particlesJS = window.particlesJS;
    if (!particlesJS) {
        console.error('particles.js library not loaded');
        return;
    }
    
    try {
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 80,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: ['#8a2be2', '#0096ff', '#ff3e9d']
                },
                shape: {
                    type: 'circle',
                    stroke: {
                        width: 0,
                        color: '#000000'
                    },
                    polygon: {
                        nb_sides: 5
                    }
                },
                opacity: {
                    value: 0.5,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 1,
                        opacity_min: 0.1,
                        sync: false
                    }
                },
                size: {
                    value: 3,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 2,
                        size_min: 0.1,
                        sync: false
                    }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#8a2be2',
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 1,
                    direction: 'none',
                    random: true,
                    straight: false,
                    out_mode: 'out',
                    bounce: false,
                    attract: {
                        enable: true,
                        rotateX: 600,
                        rotateY: 1200
                    }
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: {
                        enable: true,
                        mode: 'grab'
                    },
                    onclick: {
                        enable: true,
                        mode: 'push'
                    },
                    resize: true
                },
                modes: {
                    grab: {
                        distance: 140,
                        line_linked: {
                            opacity: 0.8
                        }
                    },
                    push: {
                        particles_nb: 3
                    }
                }
            },
            retina_detect: true
        });
        console.log('particles.js initialized');
    } catch (error) {
        console.error('Error initializing particles.js:', error);
    }
}

// Show error message
function showErrorMessage(message) {
    const errorEl = document.getElementById('form-error');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
    } else {
        console.error(message);
    }
}

// Hide error message
function hideErrorMessage() {
    const errorEl = document.getElementById('form-error');
    if (errorEl) {
        errorEl.classList.add('hidden');
    }
}

// Add responsive handlers
function addResponsiveHandlers() {
    // Resize handler for canvases
    window.addEventListener('resize', debounce(function() {
        resizeCanvases();
        
        // Redraw any active visualizations
        if (document.getElementById('visualization').classList.contains('active')) {
            updateVisualizations();
        }
    }, 250));
    
    console.log('Responsive handlers added');
}

// Resize canvases to match their container size
function resizeCanvases() {
    const canvases = document.querySelectorAll('canvas');
    canvases.forEach(canvas => {
        const container = canvas.parentElement;
        if (container) {
            const rect = container.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                // Only resize if dimensions are valid
                canvas.width = rect.width;
                canvas.height = Math.min(rect.width * 0.6, rect.height);
            }
        }
    });
}

// Debounce function to limit how often a function is called
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
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

// Create datalist element for city suggestions
function createDatalist() {
    // Check if datalist already exists
    if (document.getElementById('city-suggestions')) {
        return document.getElementById('city-suggestions');
    }
    
    const datalist = document.createElement('datalist');
    datalist.id = 'city-suggestions';
    document.body.appendChild(datalist);
    
    const cityInput = document.getElementById('birth-city');
    if (cityInput) {
        cityInput.setAttribute('list', 'city-suggestions');
        console.log('City datalist initialized');
    } else {
        console.error('City input field not found');
    }
    
    return datalist;
}

// Cleanup previous instance
const cleanupRegistry = new FinalizationRegistry(canvasId => {
    const canvas = domCache.visualizationCanvases.get(canvasId);
    if (canvas) {
        canvas.ctx = null;
        domCache.visualizationCanvases.delete(canvasId);
    }
});

// ======== NARRATIVE INERTIA TENSOR ========
function initNarrativeInertiaTensor() {
    const canvas = document.getElementById('inertia-tensor-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const perturbationInput = document.getElementById('perturbation-amplitude');
    const inertiaInput = document.getElementById('inertia-coefficient');
    const stabilityIndex = document.getElementById('stability-index');
    const eigenvalueSpectrum = document.getElementById('eigenvalue-spectrum');
    
    // Initial values
    let perturbation = parseFloat(perturbationInput.value) || 0.3;
    let inertia = parseFloat(inertiaInput.value) || 0.6;
    
    // Inertia field data
    const fieldPoints = generateInertiaField();
    
    // Update the tensor visualization
    function updateInertiaTensor() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw background grid
        drawInertiaGrid(ctx, canvas.width, canvas.height);
        
        // Calculate tensor properties based on inputs
        const stability = calculateStabilityIndex(inertia, perturbation);
        const eigenvalues = calculateEigenvalues(inertia, perturbation);
        
        // Draw tensor field visualization
        drawTensorField(ctx, fieldPoints, inertia, perturbation);
        
        // Update readouts
        stabilityIndex.textContent = stability.toFixed(2);
        eigenvalueSpectrum.textContent = `[${eigenvalues.map(v => v.toFixed(2)).join(', ')}]`;
    }
    
    // Generate points for inertia field
    function generateInertiaField() {
        const points = [];
        const density = 15;
        
        for (let x = 0; x < density; x++) {
            for (let y = 0; y < density/2; y++) {
                points.push({
                    x: (x / density) * canvas.width,
                    y: (y / (density/2)) * canvas.height,
                    strength: Math.random(), // Random initial strength
                    phase: Math.random() * Math.PI * 2 // Random phase
                });
            }
        }
        
        return points;
    }
    
    // Draw background grid
    function drawInertiaGrid(ctx, width, height) {
        ctx.strokeStyle = 'rgba(138, 43, 226, 0.1)';
        ctx.lineWidth = 1;
        
        // Draw vertical lines
        for (let x = 0; x <= width; x += 50) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        
        // Draw horizontal lines
        for (let y = 0; y <= height; y += 50) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
    }
    
    // Draw tensor field visualization
    function drawTensorField(ctx, points, inertia, perturbation) {
        // Set styles
        ctx.lineWidth = 2;
        
        // For each point in the field
        points.forEach(point => {
            // Calculate vector direction and magnitude based on inertia and perturbation
            const angle = point.phase + (Math.sin(point.x / 50) * perturbation * Math.PI);
            const length = 20 + (point.strength * 20 * inertia);
            
            // Calculate vector endpoints
            const startX = point.x - (Math.cos(angle) * length / 2);
            const startY = point.y - (Math.sin(angle) * length / 2);
            const endX = point.x + (Math.cos(angle) * length / 2);
            const endY = point.y + (Math.sin(angle) * length / 2);
            
            // Draw tensor line
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            
            // Create gradient for the line
            const gradient = ctx.createLinearGradient(startX, startY, endX, endY);
            gradient.addColorStop(0, `rgba(255, 62, 157, ${inertia})`);
            gradient.addColorStop(1, `rgba(54, 226, 120, ${perturbation})`);
            ctx.strokeStyle = gradient;
            ctx.stroke();
            
            // Draw tensor endpoints
            ctx.beginPath();
            ctx.arc(endX, endY, 2, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(54, 226, 120, 0.8)';
            ctx.fill();
        });
    }
    
    // Calculate stability index based on inertia and perturbation
    function calculateStabilityIndex(inertia, perturbation) {
        return inertia / (perturbation + 0.1) * (1 - Math.abs(inertia - 0.5));
    }
    
    // Calculate eigenvalues
    function calculateEigenvalues(inertia, perturbation) {
        // Simplified eigenvalue calculation for visualization
        const base = [3.14, 2.71, 1.62]; // Pi, e, golden ratio as base values
        
        return base.map((value, i) => {
            // Modify base values based on inertia and perturbation
            if (i === 0) return value * (1 + (inertia - 0.5) * 0.5);
            if (i === 1) return value * (1 - (perturbation - 0.5) * 0.5);
            return value * (1 + (inertia * perturbation - 0.25) * 0.5);
        });
    }
    
    // Event listeners for controls
    perturbationInput.addEventListener('input', function() {
        perturbation = parseFloat(this.value);
        updateInertiaTensor();
    });
    
    inertiaInput.addEventListener('input', function() {
        inertia = parseFloat(this.value);
        updateInertiaTensor();
    });
    
    // Initial render
    updateInertiaTensor();
}

// ======== RETRODICTIVE ATTRACTOR COLLAPSE ========
function initRetrodictiveAttractorCollapse() {
    const container = document.getElementById('attractor-collapse-container');
    const markers = document.getElementById('collapse-markers');
    const cursor = document.getElementById('collapse-cursor');
    const trigger = document.getElementById('collapse-trigger');
    const modeBtns = document.querySelectorAll('.collapse-btn[data-mode]');
    
    if (!container || !markers || !cursor || !trigger) return;
    
    // Init Three.js scene
    const width = container.clientWidth;
    const height = container.clientHeight || 300;
    
    // Create canvas if it doesn't exist
    let canvas = container.querySelector('canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        container.appendChild(canvas);
    }
    
    const ctx = canvas.getContext('2d');
    let collapseMode = 'retro'; // Default mode
    let particles = [];
    let attractors = [];
    let isCollapsing = false;
    let collapseProgress = 0;
    let animationId = null;
    
    // Generate random particles
    function generateParticles(count = 200) {
        particles = [];
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 2 + 1,
                color: getRandomColor(),
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                collapsed: false,
                originalX: 0,
                originalY: 0
            });
        }
    }
    
    // Generate timeline markers
    function generateTimelineMarkers() {
        markers.innerHTML = '';
        const count = 8;
        
        for (let i = 0; i < count; i++) {
            const marker = document.createElement('div');
            marker.className = 'collapse-marker';
            markers.appendChild(marker);
        }
    }
    
    // Generate attractors
    function generateAttractors(count = 3) {
        attractors = [];
        
        for (let i = 0; i < count; i++) {
            attractors.push({
                x: Math.random() * width,
                y: Math.random() * height,
                strength: Math.random() * 0.5 + 0.5,
                radius: Math.random() * 20 + 10,
                color: getRandomColor()
            });
        }
    }
    
    // Draw an attractor
    function drawAttractor(ctx, attractor) {
        // Glow effect
        const gradient = ctx.createRadialGradient(
            attractor.x, attractor.y, 0,
            attractor.x, attractor.y, attractor.radius * 2
        );
        gradient.addColorStop(0, attractor.color + 'AA');
        gradient.addColorStop(0.7, attractor.color + '33');
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(attractor.x, attractor.y, attractor.radius * 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Core
        ctx.fillStyle = attractor.color;
        ctx.beginPath();
        ctx.arc(attractor.x, attractor.y, attractor.radius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw a particle
    function drawParticle(ctx, particle) {
        ctx.fillStyle = particle.color;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Start the collapse animation
    function triggerCollapse() {
        if (isCollapsing) return;
        
        isCollapsing = true;
        collapseProgress = 0;
        
        // Save original positions for particles
        particles.forEach(particle => {
            particle.originalX = particle.x;
            particle.originalY = particle.y;
            particle.collapsed = false;
        });
        
        // Move cursor to beginning
        cursor.style.left = '10%';
        
        // Animate collapse
        collapseAnimation();
    }
    
    // Animation loop for collapse
    function collapseAnimation() {
        // Increment progress
        collapseProgress += 0.01;
        if (collapseProgress >= 1) {
            isCollapsing = false;
            cursor.style.left = '90%';
            return;
        }
        
        // Update cursor position during animation
        let cursorPos;
        if (collapseMode === 'retro') {
            cursorPos = 90 - collapseProgress * 80;
        } else if (collapseMode === 'forward') {
            cursorPos = 10 + collapseProgress * 80;
        } else { // bidirectional
            cursorPos = 50;
        }
        cursor.style.left = `${cursorPos}%`;
        
        requestAnimationFrame(collapseAnimation);
    }
    
    // Update particles based on attractors
    function updateParticles() {
        particles.forEach(particle => {
            // Apply attractor forces only during collapse or if bidirectional
            if (isCollapsing || collapseMode === 'bidirectional') {
                attractors.forEach(attractor => {
                    // Calculate direction to attractor
                    const dx = attractor.x - particle.x;
                    const dy = attractor.y - particle.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    // Skip if too close (already collapsed to this attractor)
                    if (distance < attractor.radius) {
                        particle.collapsed = true;
                        return;
                    }
                    
                    // Apply force based on mode
                    let forceFactor = 0;
                    if (collapseMode === 'retro') {
                        forceFactor = 0.01 * attractor.strength * (1 - collapseProgress);
                    } else if (collapseMode === 'forward') {
                        forceFactor = 0.01 * attractor.strength * collapseProgress;
                    } else { // bidirectional
                        forceFactor = 0.005 * attractor.strength;
                    }
                    
                    // Inverse square law
                    const force = forceFactor / (distance * distance);
                    
                    // Apply force
                    particle.vx += dx * force;
                    particle.vy += dy * force;
                });
            }
            
            // Apply velocity
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Add slight dampening
            particle.vx *= 0.98;
            particle.vy *= 0.98;
            
            // Boundary conditions
            if (particle.x < 0 || particle.x > width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > height) particle.vy *= -1;
        });
    }
    
    // Main render loop
    function render() {
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw particles
        particles.forEach(particle => {
            drawParticle(ctx, particle);
        });
        
        // Draw attractors
        attractors.forEach(attractor => {
            drawAttractor(ctx, attractor);
        });
        
        // Update particle positions
        updateParticles();
        
        // Continue animation
        animationId = requestAnimationFrame(render);
    }
    
    // Event listeners
    trigger.addEventListener('click', triggerCollapse);
    
    // Mode buttons
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all mode buttons
            modeBtns.forEach(b => b.classList.remove('active'));
            
            // Set active class on clicked button
            btn.classList.add('active');
            
            // Update mode
            collapseMode = btn.dataset.mode;
            
            // Reset animation if ongoing
            if (isCollapsing) {
                isCollapsing = false;
                collapseProgress = 0;
                cursor.style.left = '50%';
            }
        });
    });
    
    // Initialize
    generateParticles();
    generateAttractors();
    generateTimelineMarkers();
    render();
    
    // Cleanup function for when component is destroyed
    return function cleanup() {
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
    };
}

// ======== ENTANGLED CHART ARRAYS ========
function initEntangledChartArrays() {
    const chartCanvases = {
        alpha: document.getElementById('chart-alpha'),
        beta: document.getElementById('chart-beta'),
        gamma: document.getElementById('chart-gamma'),
        delta: document.getElementById('chart-delta')
    };
    
    const synchronizeBtn = document.getElementById('synchronize-charts');
    const resetBtn = document.getElementById('reset-charts');
    const entanglementLines = document.getElementById('entanglement-lines');
    
    // Ensure all elements exist
    if (!chartCanvases.alpha || !synchronizeBtn || !resetBtn || !entanglementLines) return;
    
    // Chart contexts
    const contexts = {};
    const chartData = {};
    const entanglementData = {};
    
    // Initialize chart data
    Object.keys(chartCanvases).forEach(key => {
        const canvas = chartCanvases[key];
        contexts[key] = canvas.getContext('2d');
        
        // Generate random data points for each chart
        chartData[key] = {
            points: generateDataPoints(30),
            color: getRandomColor(),
            entangled: false,
            phase: Math.random() * Math.PI * 2,
            frequency: 0.5 + Math.random() * 2
        };
    });
    
    // Generate random data points
    function generateDataPoints(count) {
        const points = [];
        for (let i = 0; i < count; i++) {
            points.push({
                x: i,
                y: Math.random() * 100
            });
        }
        return points;
    }
    
    // Generate entanglement lines
    function generateEntanglementLines() {
        entanglementLines.innerHTML = '';
        
        // Get all chart cells
        const chartCells = document.querySelectorAll('.chart-cell');
        
        // Create connections between charts based on entanglement
        Object.keys(chartData).forEach(sourceKey => {
            if (!chartData[sourceKey].entangled) return;
            
            // Find connected charts
            Object.keys(chartData).forEach(targetKey => {
                if (sourceKey === targetKey || !chartData[targetKey].entangled) return;
                
                // Create connection line
                if (entanglementData[`${sourceKey}-${targetKey}`] || 
                    entanglementData[`${targetKey}-${sourceKey}`]) {
                    // Connection already exists
                    return;
                }
                
                // Store entanglement connection
                entanglementData[`${sourceKey}-${targetKey}`] = {
                    source: sourceKey,
                    target: targetKey,
                    strength: Math.random() * 0.5 + 0.5 // Random strength between 0.5 and 1
                };
            });
        });
    }
    
    // Draw a chart
    function drawChart(ctx, data, width, height, time) {
        ctx.clearRect(0, 0, width, height);
        
        // Draw background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(0, 0, width, height);
        
        // Draw grid lines
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        
        // Vertical grid lines
        for (let x = 0; x <= width; x += 20) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        
        // Horizontal grid lines
        for (let y = 0; y <= height; y += 20) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        // Prepare to draw data points
        ctx.strokeStyle = data.entangled ? '#00ffff' : data.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        // Draw line connecting points
        const points = data.points;
        const xScale = width / (points.length - 1);
        const yScale = height / 120;
        
        // Apply time-based oscillation if entangled
        points.forEach((point, i) => {
            let y;
            
            if (data.entangled) {
                // Apply quantum oscillation for entangled charts
                const oscillation = 20 * Math.sin(data.phase + time * data.frequency + i * 0.2);
                y = height - ((point.y + oscillation) * yScale);
            } else {
                y = height - (point.y * yScale);
            }
            
            const x = i * xScale;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        // Stroke the line
        ctx.stroke();
        
        // Add glow effect for entangled charts
        if (data.entangled) {
            ctx.save();
            ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
            ctx.lineWidth = 6;
            ctx.shadowColor = '#00ffff';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            
            points.forEach((point, i) => {
                const oscillation = 20 * Math.sin(data.phase + time * data.frequency + i * 0.2);
                const y = height - ((point.y + oscillation) * yScale);
                const x = i * xScale;
                
                if (i === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            
            ctx.stroke();
            ctx.restore();
        }
    }
    
    // Reset all charts to non-entangled state
    function resetCharts() {
        Object.keys(chartData).forEach(key => {
            chartData[key].entangled = false;
            chartData[key].points = generateDataPoints(30);
        });
        
        // Clear entanglement data
        Object.keys(entanglementData).forEach(key => delete entanglementData[key]);
        
        // Update entanglement correlation display
        updateCorrelationDisplay();
    }
    
    // Synchronize selected charts
    function synchronizeCharts() {
        // Randomly select charts to entangle
        const chartKeys = Object.keys(chartData);
        const entangledCount = Math.floor(Math.random() * 2) + 2; // 2-3 entangled charts
        
        // Reset entanglement state
        chartKeys.forEach(key => {
            chartData[key].entangled = false;
        });
        
        // Clear existing entanglement data
        Object.keys(entanglementData).forEach(key => delete entanglementData[key]);
        
        // Shuffle and select random charts to entangle
        const shuffled = [...chartKeys].sort(() => 0.5 - Math.random());
        shuffled.slice(0, entangledCount).forEach(key => {
            chartData[key].entangled = true;
        });
        
        // Generate new entanglement connections
        generateEntanglementLines();
        
        // Update entanglement correlation display
        updateCorrelationDisplay();
    }
    
    // Update the correlation display in the chart titles
    function updateCorrelationDisplay() {
        Object.keys(chartData).forEach(key => {
            const correlationElement = document.querySelector(`#chart-${key}`).parentNode.querySelector('.chart-entanglement');
            if (correlationElement) {
                if (chartData[key].entangled) {
                    const correlation = (0.7 + Math.random() * 0.3).toFixed(2);
                    correlationElement.textContent = `ψ-correlation: ${correlation}`;
                    correlationElement.style.color = '#00ffff';
                } else {
                    correlationElement.textContent = `ψ-correlation: ${(Math.random() * 0.5).toFixed(2)}`;
                    correlationElement.style.color = '';
                }
            }
        });
    }
    
    // Animation loop
    let startTime = null;
    let animationId = null;
    
    function animate(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = (timestamp - startTime) / 1000; // Convert to seconds
        
        // Draw each chart
        Object.keys(chartCanvases).forEach(key => {
            const canvas = chartCanvases[key];
            drawChart(contexts[key], chartData[key], canvas.width, canvas.height, elapsed);
        });
        
        // Continue animation
        animationId = requestAnimationFrame(animate);
    }
    
    // Event listeners
    synchronizeBtn.addEventListener('click', synchronizeCharts);
    resetBtn.addEventListener('click', resetCharts);
    
    // Initialize charts
    Object.keys(chartCanvases).forEach(key => {
        const canvas = chartCanvases[key];
        // Set canvas dimensions if needed
        if (!canvas.width || !canvas.height) {
            canvas.width = canvas.clientWidth || 220;
            canvas.height = canvas.clientHeight || 120;
        }
    });
    
    // Start animation
    animationId = requestAnimationFrame(animate);
    
    // Return cleanup function
    return function cleanup() {
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
    };
}

// ======== NARRATIVE ECHO VIEWER ========
function initEchoViewer() {
    const echoCanvas = document.querySelector('.echo-canvas');
    const timeline = document.getElementById('echo-timeline');
    const symbolismContent = document.querySelector('.symbolism-content');
    
    if (!echoCanvas || !timeline || !symbolismContent) return;
    
    // Initialize advanced quantum features
    initNarrativeInertiaTensor();
    initRetrodictiveAttractorCollapse();
    initEntangledChartArrays();
    
    // Generate quantum states for visualization
    const events = generateRandomEvents();
    const pastEvents = generateRandomEvents();
    const futureEvents = generateRandomEvents();
    
    // Setup SVG filter for glow effects
    const svg = d3.select('.echo-canvas');
    
    // Add glow filter definition if it doesn't exist
    if (!document.querySelector('#glow-filter')) {
        const filter = svg.append('defs').append('filter')
            .attr('id', 'glow-filter')
            .attr('x', '-50%')
            .attr('y', '-50%')
            .attr('width', '200%')
            .attr('height', '200%');
            
        filter.append('feGaussianBlur')
            .attr('stdDeviation', '2.5')
            .attr('result', 'coloredBlur');
            
        const feMerge = filter.append('feMerge');
        feMerge.append('feMergeNode').attr('in', 'coloredBlur');
        feMerge.append('feMergeNode').attr('in', 'SourceGraphic');
    }
    
    // Draw the echo visualization
    function drawEchoVisualization(timeValue) {
        svg.selectAll('*:not(defs)').remove();
        
        // Center line representing the present
        svg.append('line')
            .attr('x1', 500)
            .attr('y1', 20)
            .attr('x2', 500)
            .attr('y2', 180)
            .attr('stroke', 'rgba(255, 255, 255, 0.2)')
            .attr('stroke-width', 1)
            .attr('stroke-dasharray', '4,4');
        
        // Draw past-future quantum connections
        for (let i = 0; i < events.length; i++) {
            const pastX = 200 - (i * 40);
            const futureX = 800 + (i * 40);
            const y = 40 + (i * 40);
            
            // Modulation by timeline value creates the temporal symmetry effect
            const modulation = Math.sin(timeValue * Math.PI * 2) * 50;
            const controlY = 100 + modulation;
            
            // Path between past and future
            const path = svg.append('path')
                .attr('d', `M${pastX},${y} C${350},${controlY} ${650},${controlY} ${futureX},${y}`)
                .attr('fill', 'none')
                .attr('stroke', getRandomColor())
                .attr('stroke-width', 2)
                .attr('opacity', 0.7)
                .attr('filter', 'url(#glow-filter)');
            
            // Animation effect
            const totalLength = path.node().getTotalLength();
            path.attr('stroke-dasharray', totalLength)
                .attr('stroke-dashoffset', totalLength)
                .transition()
                .duration(1000)
                .attr('stroke-dashoffset', 0);
            
            // Add dots for events
            svg.append('circle')
                .attr('cx', pastX)
                .attr('cy', y)
                .attr('r', 5)
                .attr('fill', getRandomColor())
                .attr('filter', 'url(#glow-filter)');
                
            svg.append('circle')
                .attr('cx', futureX)
                .attr('cy', y)
                .attr('r', 5)
                .attr('fill', getRandomColor())
                .attr('filter', 'url(#glow-filter)');
        }
    }
    
    // Update the symbolic interpretation
    function updateSymbolicInterpretation(timeValue) {
        // Generate symmetry pairs based on the timeline value
        const normalized = timeValue.toFixed(2);
        const pastSymbols = pastEvents.map(e => e.type);
        const futureSymbols = futureEvents.map(e => e.type);
        
        let html = `<p>Temporal Symmetry Value: ${normalized}</p><div class="echo-pairs">`;
        
        // Create symbolic pairs between past and future
        for (let i = 0; i < Math.min(pastSymbols.length, futureSymbols.length); i++) {
            const resonance = ((1 - Math.abs(timeValue - 0.5) * 2) * 100).toFixed(0);
            html += `
                <div class="echo-pair">
                    <span class="past-symbol">${pastSymbols[i]}</span>
                    <span class="resonance-value">${resonance}% Resonance</span>
                    <span class="future-symbol">${futureSymbols[i]}</span>
                </div>
            `;
        }
        
        html += '</div>';
        symbolismContent.innerHTML = html;
    }
    
    // Initial draw
    drawEchoVisualization(0.5);
    updateSymbolicInterpretation(0.5);
    
    // Update on timeline change
    timeline.addEventListener('input', function() {
        const timeValue = parseFloat(this.value);
        drawEchoVisualization(timeValue);
        updateSymbolicInterpretation(timeValue);
    });
}
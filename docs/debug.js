// Debug script for ASTRA website
document.addEventListener('DOMContentLoaded', function() {
    console.log('Debug script loaded');
    
    // Check if required libraries are loaded
    const libraries = {
        'three.js': window.THREE,
        'd3.js': window.d3,
        'gsap': window.gsap,
        'particles.js': window.particlesJS,
        'force-graph': window.ForceGraph
    };
    
    console.log('Library status:');
    for (const [name, lib] of Object.entries(libraries)) {
        console.log(`${name}: ${lib ? 'Loaded' : 'NOT LOADED'}`);
    }
    
    // Check if DOM elements exist
    const elements = [
        'cosmic-canvas',
        'particles-js',
        'birth-data-form',
        'visualization-container'
    ];
    
    console.log('DOM elements:');
    elements.forEach(id => {
        const element = document.getElementById(id);
        console.log(`#${id}: ${element ? 'Found' : 'NOT FOUND'}`);
    });
    
    // Test tab functionality
    const tabs = document.querySelectorAll('.tab-btn');
    console.log(`Found ${tabs.length} tabs`);
    
    // Add manual tab functionality to ensure it works
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            console.log(`Tab clicked: ${this.getAttribute('data-tab')}`);
            
            // Remove active class from all tabs and panes
            document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            
            // Add active class to current tab and corresponding pane
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            const pane = document.getElementById(tabId);
            if (pane) {
                pane.classList.add('active');
                console.log(`Activated pane: ${tabId}`);
            } else {
                console.error(`Pane not found: ${tabId}`);
            }
        });
    });
    
    // Test form functionality
    const form = document.getElementById('birth-data-form');
    if (form) {
        console.log('Form found, adding test handler');
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Form submitted');
            
            // Collect form data
            const formData = {
                name: document.getElementById('name')?.value,
                birthDate: document.getElementById('birth-date')?.value,
                birthTime: document.getElementById('birth-time')?.value,
                birthCity: document.getElementById('birth-city')?.value,
                birthCountry: document.getElementById('birth-country')?.value
            };
            
            console.log('Form data:', formData);
            
            // Show results tab
            const resultsTab = document.querySelector('.tab-btn[data-tab="results"]');
            if (resultsTab) {
                resultsTab.click();
                console.log('Switched to results tab');
            }
        });
    }
    
    // Add submit button functionality
    const submitBtn = document.querySelector('.submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            console.log('Submit button clicked');
            if (form) form.dispatchEvent(new Event('submit'));
        });
    }
});

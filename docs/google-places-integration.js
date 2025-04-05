/**
 * ASTRA - Google Places API Integration
 * Provides global city search with high precision geolocation data
 */

// Initialize Google Places Autocomplete when the Google Maps API is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Waiting for Google Places API to load');
    
    // Check if API is already loaded
    if (window.google && window.google.maps && window.google.maps.places) {
        console.log('Google Places API already loaded');
        initGooglePlacesAutocomplete();
        return;
    }
    
    // Set up a listener for when the API loads
    window.initGooglePlaces = function() {
        console.log('Google Places API loaded');
        initGooglePlacesAutocomplete();
    };
    
    // Check periodically if the API has loaded
    const checkGoogleMapsLoaded = setInterval(function() {
        if (window.google && window.google.maps && window.google.maps.places) {
            clearInterval(checkGoogleMapsLoaded);
            console.log('Google Places API detected');
            initGooglePlacesAutocomplete();
        }
    }, 100);
});

/**
 * Initialize Google Places Autocomplete for the birth city input
 */
function initGooglePlacesAutocomplete() {
    // Get the input element
    const cityInput = document.getElementById('birth-city');
    const latInput = document.getElementById('birth-city-lat');
    const lngInput = document.getElementById('birth-city-lng');
    
    if (!cityInput) {
        console.error('Birth city input not found');
        return;
    }
    
    // Check if Google Places API is loaded
    if (!window.google || !window.google.maps || !window.google.maps.places) {
        console.error('Google Places API not loaded. Please check your API key.');
        
        // Add a visual indicator that the API is not loaded
        cityInput.classList.add('api-error');
        
        // Show a more helpful message based on the environment
        if (window.location.hostname.includes('github.io')) {
            cityInput.setAttribute('placeholder', 'API key not set in GitHub Secrets');
            console.warn('For GitHub Pages: Add GOOGLE_API_KEY to repository secrets');
        } else {
            cityInput.setAttribute('placeholder', 'Google Places API not loaded');
            console.warn('For local development: Create config.js with your API key');
        }
        
        // Fall back to basic input
        setupBasicCityInput(cityInput);
        return;
    }
    
    try {
        // Create the autocomplete object, restricting the search to geographical
        // location types (cities, regions, etc.)
        const autocomplete = new google.maps.places.Autocomplete(cityInput, {
            types: ['(cities)'],
            fields: ['address_components', 'geometry', 'name', 'formatted_address']
        });
        
        // When a place is selected, populate the hidden fields with lat/lng
        autocomplete.addListener('place_changed', function() {
            const place = autocomplete.getPlace();
            
            if (!place.geometry) {
                console.warn('No geometry information available for selected place');
                return;
            }
            
            // Store latitude and longitude in hidden fields
            if (latInput) latInput.value = place.geometry.location.lat();
            if (lngInput) lngInput.value = place.geometry.location.lng();
            
            // Extract and store city, state/province, and country information
            let city = '';
            let state = '';
            let country = '';
            let countryCode = '';
            
            for (const component of place.address_components) {
                const types = component.types;
                
                if (types.includes('locality')) {
                    city = component.long_name;
                } else if (types.includes('administrative_area_level_1')) {
                    state = component.long_name;
                } else if (types.includes('country')) {
                    country = component.long_name;
                    countryCode = component.short_name;
                }
            }
            
            // Update country dropdown if available
            const countrySelect = document.getElementById('birth-country');
            if (countrySelect && countryCode) {
                // Try to select the matching country option
                const options = countrySelect.options;
                for (let i = 0; i < options.length; i++) {
                    if (options[i].value === countryCode) {
                        countrySelect.selectedIndex = i;
                        break;
                    }
                }
            }
            
            // Log the selected place details
            console.log('Selected place:', {
                name: place.name,
                formattedAddress: place.formatted_address,
                lat: place.geometry.location.lat(),
                lng: place.geometry.location.lng(),
                city,
                state,
                country,
                countryCode
            });
            
            // Dispatch a custom event for other components to react to
            const event = new CustomEvent('placeSelected', {
                detail: {
                    name: place.name,
                    formattedAddress: place.formatted_address,
                    lat: place.geometry.location.lat(),
                    lng: place.geometry.location.lng(),
                    city,
                    state,
                    country,
                    countryCode
                }
            });
            document.dispatchEvent(event);
        });
        
        // Prevent form submission when Enter is pressed in the autocomplete field
        cityInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && autocomplete.getPlace === undefined) {
                e.preventDefault();
            }
        });
        
        // Add custom styling to the Google Places autocomplete dropdown
        customizeAutocompleteStyles();
        
        console.log('Google Places Autocomplete initialized successfully');
    } catch (error) {
        console.error('Error initializing Google Places Autocomplete:', error);
        setupBasicCityInput(cityInput);
    }
}

/**
 * Set up a basic city input with datalist as fallback
 * @param {HTMLInputElement} cityInput - The city input element
 */
function setupBasicCityInput(cityInput) {
    console.log('Setting up basic city input as fallback');
    
    // Create a datalist element for basic autocomplete
    const datalistId = 'city-datalist';
    let datalist = document.getElementById(datalistId);
    
    if (!datalist) {
        datalist = document.createElement('datalist');
        datalist.id = datalistId;
        document.body.appendChild(datalist);
        
        // Add some major cities as options
        const majorCities = [
            'New York, USA', 'London, UK', 'Tokyo, Japan', 'Paris, France',
            'Beijing, China', 'Moscow, Russia', 'Sydney, Australia', 'Cairo, Egypt',
            'Rio de Janeiro, Brazil', 'Mumbai, India', 'Toronto, Canada',
            'Berlin, Germany', 'Mexico City, Mexico', 'Cape Town, South Africa',
            'Seoul, South Korea', 'Rome, Italy', 'Istanbul, Turkey'
        ];
        
        majorCities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            datalist.appendChild(option);
        });
    }
    
    // Connect the datalist to the input
    cityInput.setAttribute('list', datalistId);
}

/**
 * Add custom styling to the Google Places autocomplete dropdown
 */
function customizeAutocompleteStyles() {
    // Create a style element to customize the Google Places autocomplete dropdown
    const styleId = 'google-places-custom-styles';
    if (document.getElementById(styleId)) return;
    
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
        /* Override Google's default styles with our theme */
        .pac-container {
            z-index: 9999 !important;
        }
    `;
    
    document.head.appendChild(style);
}

/**
 * Get timezone information for a location
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @param {function} callback - Callback function to handle the result
 */
function getTimezoneForLocation(lat, lng, callback) {
    if (!window.google || !window.google.maps) {
        console.error('Google Maps API not loaded');
        callback(null);
        return;
    }
    
    const timestamp = Math.floor(Date.now() / 1000);
    const location = new google.maps.LatLng(lat, lng);
    
    const timezone = new google.maps.TimeZoneService();
    timezone.getTimeZoneAtLocation(location, timestamp, function(result) {
        if (result.status === 'OK') {
            callback(result);
        } else {
            console.error('Timezone API error:', result.status);
            callback(null);
        }
    });
}

/**
 * Calculate the local time at a specific location
 * @param {Date} utcTime - UTC time
 * @param {number} timezoneOffset - Timezone offset in minutes
 * @param {boolean} dstOffset - Daylight saving time offset in minutes
 * @returns {Date} Local time at the specified location
 */
function calculateLocalTime(utcTime, timezoneOffset, dstOffset) {
    const totalOffset = (timezoneOffset + dstOffset) * 60 * 1000;
    return new Date(utcTime.getTime() + totalOffset);
}

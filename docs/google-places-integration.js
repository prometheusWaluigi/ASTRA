/**
 * ASTRA - Google Places API Integration
 * Provides global city search with high precision geolocation data
 */

// Initialize Google Places Autocomplete when the Google Maps API is loaded
let placeAutocompleteElementInstance = null; // To hold the instance for dynamic updates

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
async function initGooglePlacesAutocomplete() { // Made async for await google.maps.importLibrary
    // Get original input element and hidden fields
    const originalCityInput = document.getElementById('birth-city');
    const latInput = document.getElementById('birth-city-lat');
    const lngInput = document.getElementById('birth-city-lng');

    if (!originalCityInput) {
        console.error('Original birth city input element not found');
        return;
    }

    // Ensure the Places library is loaded
    try {
        if (!google.maps.places) {
            console.log('Places library not found directly, attempting to import...');
            await google.maps.importLibrary("places");
            console.log('Places library imported successfully.');
        }
    } catch (e) {
        console.error('Error importing Google Places library:', e);
        if (originalCityInput) setupBasicCityInput(originalCityInput); // Fallback for original input
        return;
    }

    // Check if Google Places API is truly available now
    if (!window.google || !window.google.maps || !window.google.maps.places || !google.maps.places.PlaceAutocompleteElement) {
        console.error('Google Places API or PlaceAutocompleteElement not available after import. Please check your API key and library loading.');
        if (originalCityInput) {
            originalCityInput.classList.add('api-error');
            if (window.location.hostname.includes('github.io')) {
                originalCityInput.setAttribute('placeholder', 'API key/config issue for new Autocomplete');
            } else {
                originalCityInput.setAttribute('placeholder', 'Google Places API (New) not loaded');
            }
            setupBasicCityInput(originalCityInput);
        }
        return;
    }

    try {
        // Create the new PlaceAutocompleteElement
        const placeAutocompleteElement = new google.maps.places.PlaceAutocompleteElement({
            types: ['(cities)'],
            // `fields` are requested later with place.fetchFields()
        });

        placeAutocompleteElementInstance = placeAutocompleteElement; // Assign to the module-scoped variable

        // Assign properties from the old input to the new element
        placeAutocompleteElement.id = originalCityInput.id; // 'birth-city'
        placeAutocompleteElement.name = originalCityInput.name;
        placeAutocompleteElement.placeholder = originalCityInput.placeholder;
        if (originalCityInput.required) {
            placeAutocompleteElement.setAttribute('required', '');
        }
        // Copy other relevant classes if any, besides 'api-error' which we handle
        originalCityInput.classList.forEach(cls => {
            if (cls !== 'api-error' && cls !== 'valid' && cls !== 'invalid') {
                placeAutocompleteElement.classList.add(cls);
            }
        });

        // Replace the old input with the new PlaceAutocompleteElement
        originalCityInput.parentNode.replaceChild(placeAutocompleteElement, originalCityInput);
        console.log('Replaced old input with PlaceAutocompleteElement.');

        // Add the event listener for when a place is selected
        placeAutocompleteElement.addEventListener('gmp-select', async (event) => {
            const placePrediction = event.placePrediction;
            if (!placePrediction) {
                console.warn('No place prediction data in gmp-select event');
                return;
            }
            const place = placePrediction.toPlace();
            
            try {
                await place.fetchFields({ fields: ['address_components', 'geometry', 'name', 'formatted_address'] });
            } catch (error) {
                console.error('Error fetching place fields:', error);
                window.alert("Could not retrieve details for the selected place. Error: " + error.message);
                return;
            }

            if (!place.geometry || !place.geometry.location) {
                console.warn('No geometry information available for selected place after fetching fields');
                // Optionally, clear hidden fields or show a message
                if (latInput) latInput.value = '';
                if (lngInput) lngInput.value = '';
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

            if (place.address_components) {
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
            }

            // Update country dropdown if available
            const countrySelect = document.getElementById('birth-country');
            if (countrySelect && countryCode) {
                const options = countrySelect.options;
                for (let i = 0; i < options.length; i++) {
                    if (options[i].value === countryCode) {
                        countrySelect.selectedIndex = i;
                        break;
                    }
                }
            }

            console.log('Selected place (New API):', {
                name: place.name || place.displayName,
                formattedAddress: place.formatted_address,
                lat: place.geometry.location.lat(),
                lng: place.geometry.location.lng(),
                city,
                state,
                country,
                countryCode
            });

            // Dispatch a custom event for other components to react to
            const customEvent = new CustomEvent('placeSelected', {
                detail: {
                    name: place.name || place.displayName,
                    formattedAddress: place.formatted_address,
                    lat: place.geometry.location.lat(),
                    lng: place.geometry.location.lng(),
                    city,
                    state,
                    country,
                    countryCode
                }
            });
            document.dispatchEvent(customEvent);
        });

        // The new PlaceAutocompleteElement handles Enter key behavior appropriately by default.
        // The old keydown listener for cityInput might not be necessary or could conflict.
        // If specific Enter key behavior is still needed, it should be tested carefully with the new element.

        // Add custom styling to the Google Places autocomplete dropdown (may need review for new element)
        // Listen for country changes to update autocomplete restrictions
        document.addEventListener('countryChanged', (event) => {
            if (placeAutocompleteElementInstance && event.detail && event.detail.country) {
                const countryCode = event.detail.country.toLowerCase(); // Ensure lowercase for API
                console.log(`Country changed to: ${countryCode}. Updating autocomplete restrictions.`);
                placeAutocompleteElementInstance.componentRestrictions = { country: countryCode };
            } else if (placeAutocompleteElementInstance && event.detail && (event.detail.country === '' || event.detail.country === null)) {
                // If country is cleared (e.g., "Select Country" is chosen or value is empty/null), remove restrictions
                console.log('Country cleared. Removing autocomplete restrictions.');
                placeAutocompleteElementInstance.componentRestrictions = null; 
            }
        });

        customizeAutocompleteStyles();
        
        console.log('Google PlaceAutocompleteElement initialized successfully');
    } catch (error) {
        console.error('Error initializing Google PlaceAutocompleteElement:', error);
        // If new element failed, try to fallback with the original (now detached) input, or a new basic one.
        const fallbackInput = document.getElementById('birth-city') || document.createElement('input');
        if (!document.getElementById('birth-city')) { // If original was removed and new one not added
            fallbackInput.id = 'birth-city';
             // Consider re-adding to DOM if it was fully removed and not replaced
        }
        setupBasicCityInput(fallbackInput);
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

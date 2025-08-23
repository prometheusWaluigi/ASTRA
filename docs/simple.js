// Simple input handling for ASTRA
async function searchCities(query) {
  const response = await fetch(`/city_search?query=${encodeURIComponent(query)}`);
  if (!response.ok) return [];
  return await response.json();
}

function getZodiacSign(month, day) {
  const signs = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) return signs[0];
  if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) return signs[1];
  if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) return signs[2];
  if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) return signs[3];
  if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) return signs[4];
  if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) return signs[5];
  if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) return signs[6];
  if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) return signs[7];
  if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) return signs[8];
  if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) return signs[9];
  if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) return signs[10];
  return signs[11];
}

document.addEventListener('DOMContentLoaded', () => {
  const cityInput = document.getElementById('city');
  const datalist = document.getElementById('city-options');

  cityInput.addEventListener('input', async () => {
    const q = cityInput.value.trim();
    if (q.length < 2) return;
    const cities = await searchCities(q);
    datalist.innerHTML = '';
    cities.forEach(c => {
      const option = document.createElement('option');
      option.value = `${c.city}, ${c.country}`;
      option.dataset.lat = c.lat;
      option.dataset.lng = c.lng;
      datalist.appendChild(option);
    });
  });

  document.getElementById('birth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const [cityName, country = ''] = cityInput.value.split(',').map(s => s.trim());
    let lat = '', lng = '';
    if (cityName && country) {
      try {
        const resp = await fetch(`/city_lookup?city=${encodeURIComponent(cityName)}&country=${encodeURIComponent(country)}`);
        const data = await resp.json();
        lat = data.lat || '';
        lng = data.lng || '';
      } catch (err) {
        console.error('Lookup failed', err);
      }
    }
    const date = document.getElementById('date').value;
    const [year, month, day] = date.split('-').map(Number);
    const analysisText = `Name: ${document.getElementById('name').value}\n` +
      `Birth Date: ${date}\n` +
      `Birth Time: ${document.getElementById('time').value}\n` +
      `Location: ${cityName}, ${country} (${lat}, ${lng})\n` +
      `Sun Sign: ${getZodiacSign(month, day)}`;
    document.getElementById('analysis').textContent = analysisText;
  });
});

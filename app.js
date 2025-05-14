async function loadData() {
    const response = await fetch('foi_summaries.json');
    const data = await response.json();
    const results = document.getElementById('results');
    const searchInput = document.getElementById('search');
  
    function displayData(filteredData) {
      results.innerHTML = '';
      filteredData.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.Title} - Theme: ${item.Theme}`;
        results.appendChild(li);
      });
    }
  
    displayData(data);
  
    searchInput.addEventListener('input', () => {
      const term = searchInput.value.toLowerCase();
      const filtered = data.filter(d => d.Title.toLowerCase().includes(term) || d.Theme.toLowerCase().includes(term));
      displayData(filtered);
    });
  }
  
  loadData();  
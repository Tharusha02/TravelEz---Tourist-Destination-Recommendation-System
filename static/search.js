window.addEventListener('DOMContentLoaded', async () => {
    try {
        await fetchData(); // Call the fetchData function on page load
    } catch (error) {
        console.error('Error populating cards:', error);
    }
});

async function fetchData() {
    try {
        const response = await fetch('/output_data'); // Fetch data from Flask server
        const data = await response.json(); // Parse JSON data
        console.log('Fetched data:', data); 
        populateCards(data); // Populate cards with fetched data
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function populateCards(data) {
    console.log('Populating cards with data:', data);
    const cards = document.querySelectorAll('.card');

    cards.forEach((card, index) => {
        const category = card.classList.contains('restaurant') ? 'restaurants' :
                         card.classList.contains('travel-agent') ? 'travel_agents' :
                         card.classList.contains('accommodation') ? 'accommodations' :
                         '';
        const cardTitle = card.querySelector('h2');
        const cardDetails = card.querySelector('p');

        if (category) {
            cardTitle.textContent = data[category][index][0];
            if (category === 'accommodations') {
                cardDetails.textContent = "Type: " + data[category][index][1];
                cardDetails.innerHTML += "<br> Address: " + data[category][index][2];
            } else {
                cardDetails.textContent = "Address: " + data[category][index][1];
                if (data[category][index][2]) {
                    cardDetails.innerHTML += "<br> Grade: " + data[category][index][2];
                }
            }
        }

        const prevButton = card.querySelector('.prev-btn');
        const nextButton = card.querySelector('.next-btn');

        prevButton.addEventListener('click', () => {
            index = (index - 1 + data[category].length) % data[category].length;
            updateCardContent(card, category, index, data);
        });

        nextButton.addEventListener('click', () => {
            index = (index + 1) % data[category].length;
            updateCardContent(card, category, index, data);
        });
    });
}

function updateCardContent(card, category, index, data) {
    const cardTitle = card.querySelector('h2');
    const cardDetails = card.querySelector('p');

    cardTitle.textContent = data[category][index][0];
    if (category === 'accommodations') {
        cardDetails.innerHTML = "Type: " + data[category][index][1] + "<br> Address: " + data[category][index][2];
    } else {
        cardDetails.textContent = "Address: " + data[category][index][1];
        if (data[category][index][2]) {
            cardDetails.innerHTML += "<br> Grade: " + data[category][index][2];
        }
    }
}

let subMenu = document.getElementById("subMenu");

        function toggleMenu(){
            subMenu.classList.toggle("open-menu")
        }


// Sample JSON data  (fetch all data from the API)
const jsonData = {
    "restaurants": [
        { "name": "Bavarian Barn Restaurant", "address": "No. 11, Galle Face Court, 02 Colombo" },
        { "name": "Lords Restaurant", "address": "80B Poruthota Road, Etthukala, Negombo" },
        { "name": "Nihonbashi Restaurant", "address": "No. 11, Galle Face Terrace, Colombo 03" },
        { "name": "Free Wind Restaurant & Bar", "address": "No. 1285, Kandy Road, Palaiyoothu, Trinco Malee" }
    ],
    "travel_agents": [
        { "name": "Exotic Tours (Pvt) Ltd", "address": "No. 572/10, 2nd Floor, Madiwela Road, Thalawathugoda" },
        { "name": "Hamoo's Travels (Pvt) Ltd", "address": "No. 34, Dr Wijewardhana Mawatha, Colombo 10" },
        { "name": "Worldlink Travels (Pvt) Ltd", "address": "No. 20 Dharmarama Road, Colombo 06" },
        { "name": "The Travel Market (Pvt) Ltd", "address": "No. 182, Airlink Towers, Main Street, Kattankudy 02" }
    ],
    "accommodations": [
        { "name": "The Theva Residency", "address": "11/B5/10-1, 6th Lane, Hantana, Kandy" },
        { "name": "Highland Villa", "address": "351, Abimangama Road, Kumbalgama, Weligama" },
        { "name": "Ulagalla Walawwa Resort", "address": "Thirappane, Anuradhapura" },
        { "name": "Galle Fort Hotel", "address": "No. 28, Church Street, Fort, Galle" },
        { "name": "The Elephant Corridor", "address": "Pothana, Kibissa, Sigiriya" }
    ],
     "destinations": [
        { "name": "Pinnawala Elephant Orphanage", "address": "B199, Rambukkana 71100, Sri Lanka" },
        { "name": "Polonnaruwa – The Ancient Ruins", "address": "Polonnaruwa District in North Central Province, Sri Lanka" },
        { "name": "Tissamaharama – Picture Worthy Place", "address": "Hambantota District, Southern Province, Sri Lanka" }
        ]
    }
    
    
    // Update the populateCards function to handle the new destination card
    function populateCards(data) {
        const cards = document.querySelectorAll('.card');
        
        cards.forEach((card, index) => {
            const category = card.classList.contains('restaurant') ? 'restaurants' :
                             card.classList.contains('travel-agent') ? 'travel_agents' :
                             card.classList.contains('accommodation') ? 'accommodations' :
                             card.classList.contains('destination') ? 'destinations' :
                             '';
    
            const cardTitle = card.querySelector('h2');
            const cardDetails = card.querySelector('p');
    
            cardTitle.textContent = data[category][index].name;
            cardDetails.textContent = "Address: " + data[category][index].address;
    
            const viewMoreButton = card.querySelector('.view-more');
            viewMoreButton.addEventListener('click', () => {
              // Increment the index to get the next item   
                index = (index + 1) % data[category].length;
                cardTitle.textContent = data[category][index].name;
                cardDetails.textContent = "Address: " + data[category][index].address;

            

        
            });
        });
    }
    
    // Entry point
window.addEventListener('DOMContentLoaded', async () => {
    try {
        populateCards(jsonData);
    } catch (error) {
        console.error('Error populating cards:', error);
    }
});

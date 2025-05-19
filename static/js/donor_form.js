document.addEventListener("DOMContentLoaded", function () {
    // Fetch State & City via ZIP Code
    // document.getElementById("id_zip_code").addEventListener("blur", function () {
    //     let zip = this.value;
    //     if (zip.length >= 5) {
    //         fetch(`https://api.zippopotam.us/in/${zip}`)
    //             .then(response => response.json())
    //             .then(data => {
    //                 document.getElementById("id_state").value = data.places[0]["state"];
    //                 document.getElementById("id_city").value = data.places[0]["place name"];
    //             })
    //             .catch(error => console.error("Error fetching ZIP code data:", error));
    //     }
    // });

    // Load Country List Alphabetically
    // fetch("https://restcountries.com/v3.1/all")
    //     .then(response => response.json())
    //     .then(data => {
    //         let countrySelect = document.getElementById("id_country");
    //         let sortedCountries = data.sort((a, b) => a.name.common.localeCompare(b.name.common));
    //         sortedCountries.forEach(country => {
    //             let option = document.createElement("option");
    //             option.value = country.name.common;
    //             option.textContent = country.name.common;
    //             countrySelect.appendChild(option);
    //         });
    //     });

    // Auto-fetch Latitude & Longitude
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            document.getElementById("id_latitude").value = position.coords.latitude;
            document.getElementById("id_longitude").value = position.coords.longitude;
        });
    }
});

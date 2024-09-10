async function onClickEstimatePrice() {
    // Get selected values from the dropdowns and input fields
    const manufacturer = document.getElementById('manufacturer').value;
    const model = document.getElementById('model').value;
    const category = document.getElementById('category').value;
    const prod_year = document.getElementById('prod_year').value;
    const mileage = document.getElementById('mileage').value;
    const levy = document.getElementById('levy').value;
    const fuel_type = document.getElementById('fuel_type').value;
    const gear_box_type = document.getElementById('gear_box_type').value;
    const color = document.getElementById('color').value;
    const engine_volume = document.getElementById('engine_volume').value;
    const drive_wheel = document.getElementById('drive_wheels').value;
    const airbag = document.getElementById('airbag').value;
    const cylinder = document.getElementById('cylinder').value;
    const interior = document.getElementById('interior').value;
    const model_choice = document.querySelector('input[name="model_choice"]:checked').value;

    const predictionSection = document.getElementById('predictionSection')

    // Validate the inputs (optional, depending on your requirements)
    if (!manufacturer || !model || !category || !prod_year || !mileage || !levy || !fuel_type ||
        !gear_box_type || !color || !engine_volume || !drive_wheels || !cylinder || !interior || !model_choice) {
        alert("Please fill out all fields.");
        return;
    }

    // Create an object with the selected values (for sending to the backend)
    const formData = {
        manufacturer: manufacturer,
        model: model,
        category: category,
        prod_year: prod_year,
        mileage: parseInt(mileage),
        levy: parseInt(levy),
        fuel_type: fuel_type,
        gear_box_type: gear_box_type,
        color: color,
        engine_volume: parseFloat(engine_volume),
        drive_wheel: drive_wheel,
        airbag: parseInt(airbag),
        cylinder: parseInt(cylinder),
        interior: interior,
        model_choice: model_choice
    };
    
    try {
        const response = await fetch('http://localhost:5000/estimate-price', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        predictionSection.innerHTML = `<h2>${result.predicted_price}</h2>`;
    } catch (error) {
        console.error('Error:', error);
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const manufacturerSelect = document.getElementById('manufacturer');
    const modelSelect = document.getElementById('model');
    const categorySelect = document.getElementById('category');
    const colorSelect = document.getElementById('color');
    const fuelTypeSelect = document.getElementById('fuel_type');
    const prodYearSelect = document.getElementById('prod_year');
    const gearBoxSelect = document.getElementById('gear_box_type');

    

    // Populate production years
    for (let year = 1999; year <= 2100; year++) {
        let option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        prodYearSelect.appendChild(option);
    }

    // Fetch data and populate dropdowns (mocked API calls)
    fetchManufacturers();
    fetchCategories();
    fetchColors();
    fetchGearBoxType();
    fetchFuelType();

    manufacturerSelect.addEventListener('change', function () {
        fetchModels(this.value);
    });

    async function fetchManufacturers() {
        const url = 'http://localhost:5000/object/manufacturers'
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Netork response was not ok');
            }
            const data = await response.json();
            if (data && data.objects) {
                let manufacturers = data.objects;

                manufacturers.sort((a, b) => a.localeCompare(b));

                manufacturerSelect.innerHTML = '<option value="" selected="selected" disabled="disabled">Select Manufacturer</option>';
                populateSelect(manufacturerSelect, manufacturers);
                let otherOption = document.createElement('option');
                otherOption.value = "other";
                otherOption.textContent = "Other";
                manufacturerSelect.appendChild(otherOption);
            }
            
        } catch (error) {
            console.error('Error: ', error)
        }
    }

    async function fetchModels(manufacturer) {
        const url = 'http://localhost:5000/manufacturer/' + manufacturer
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not OK!')
            }
            const data = await response.json()
            if (data && data[manufacturer]) {
                let models = data[manufacturer]

                models.sort((a,b) => a.localeCompare(b));

                modelSelect.innerHTML = '<option value="" selected="selected" disabled="disabled">Select Model</option>';
                populateSelect(modelSelect, models || []);
                modelSelect.innerHTML += '<option value="other">Other</option>';
            }
        } catch (error) {
            console.error('Error: ', error)
        }
    }

    async function fetchCategories() {
        const url = 'http://localhost:5000/object/categories';
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            if (data && data.objects) {
                let categories = data.objects;
                
                // Sort categories alphabetically
                categories.sort((a, b) => a.localeCompare(b));
    
                // Clear existing options and populate the select dropdown
                categorySelect.innerHTML = '<option value="" selected="selected" disabled="disabled">Select Category</option>';
                populateSelect(categorySelect, categories);
                let otherOption = document.createElement('option');
                otherOption.value = "other";
                otherOption.textContent = "Other";
                categorySelect.appendChild(otherOption);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    

    async function fetchColors() {
        const url = 'http://localhost:5000/object/colors';
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            if (data && data.objects) {
                let colors = data.objects;
                
                // Sort colors alphabetically
                colors.sort((a, b) => a.localeCompare(b));
    
                // Clear existing options and populate the select dropdown
                colorSelect.innerHTML = '<option value="" selected="selected" disabled="disabled">Select Color</option>';
                populateSelect(colorSelect, colors);
                let otherOption = document.createElement('option');
                otherOption.value = "other";
                otherOption.textContent = "Other";
                colorSelect.appendChild(otherOption);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    async function fetchGearBoxType() {
        const url = 'http://localhost:5000/object/gear_boxes';

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok!')
            }
            const data = await response.json()
            if (data && data.objects) {
                let gear_boxes = data.objects;

                gear_boxes.sort((a,b) => a.localeCompare(b))

                gearBoxSelect.innerHTML = '<option value="" selected="selected" disabled="disabled">Select Gear Box</option>';
                populateSelect(gearBoxSelect, gear_boxes);
                let otherOption = document.createElement('option');
                otherOption.value = "other";
                otherOption.textContent = "Other";
                gearBoxSelect.appendChild(otherOption);
            }
        } catch (error) {
            console.error('Error: ', error)
        }
    }

    async function fetchFuelType() {
        const url = 'http://localhost:5000/object/fuels';

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not OK!')
            }
            const data = await response.json()

            if (data && data.objects) {
                let fuels = data.objects;

                fuels.sort((a,b) => a.localeCompare(b));
                fuelTypeSelect.innerHTML = '<option value="" selected="selected" disabled="disabled">Select Fuel Type</option>';
                populateSelect(fuelTypeSelect, fuels);
                let otherOption = document.createElement('option');
                otherOption.value = 'other';
                otherOption.textContent = 'Other';
                fuelTypeSelect.appendChild(otherOption);
            }
        } catch (error) {
            console.error('Error: ', error);
        }
    }

    function populateSelect(selectElement, options) {
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.value = option.toLowerCase();
            opt.textContent = option;
            selectElement.appendChild(opt);
        });
    }
});

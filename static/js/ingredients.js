var numberOfIngredients = 1;

function setNumberOfIngredients() {
	document.getElementById("number_of_ingredients").value = numberOfIngredients;
}

function addIngredient(event) {
	event.preventDefault();

	// Get holder for ingredients
	var holder = document.getElementById("ingredients");

	// Create div for new ingredient
	var div = document.createElement("DIV");
	div.classList.add("ingredient-div");
	div.setAttribute("id", "ingredient-div-" + numberOfIngredients);

	// Create input for ingredient name
	var name = document.createElement("INPUT");
	name.classList.add("ingredient-input");
	name.setAttribute("type", "text");
	name.setAttribute("id", "ingredient-name-" + numberOfIngredients);
	name.setAttribute("name", "ingredient-name-" + numberOfIngredients);
	name.setAttribute("placeholder", "Ingredient");
	div.appendChild(name);

	// Create input for ingredient quantity
	var amount = document.createElement("INPUT");
	amount.classList.add("ingredient-input");
	amount.setAttribute("type", "number");
	amount.setAttribute("step", "0.01");
	amount.setAttribute("id", "ingredient-quantity-" + numberOfIngredients);
	amount.setAttribute("name", "ingredient-quantity-" + numberOfIngredients);
	amount.setAttribute("placeholder", "Quantity");
	div.appendChild(amount);

	// units array
	var database_units = ["tbsp", "tsp", "cup", "pinch", "l", "ml", "g", "kg"];
	var display_units = ["Tablespoon", "Teaspoon", "Cup", "Pinch", "Litre", "Millilitre", "Gram", "Kilogram"]

	// Create input for ingredient quantity unit
	var unit = document.createElement("SELECT");
	unit.classList.add("ingredient-input");
	for(var i = 0; i < 8; i++) {
		var option = document.createElement("OPTION");
		option.value = database_units[i];
		option.text = display_units[i];
		unit.appendChild(option);
	}
	unit.setAttribute("id", "ingredient-unit-" + numberOfIngredients);
	unit.setAttribute("name", "ingredient-unit-" + numberOfIngredients);
	div.appendChild(unit);

	var button = document.createElement("BUTTON");
	button.classList.add("ingredient-button");
	button.setAttribute("id", "ingredient-button-" + numberOfIngredients);
	button.addEventListener("click", function(event) {
		event.preventDefault();
		var res = this.id.split('-');
		var elementId = res[res.length - 1];
		removeIngredient(elementId);
	});
	var textForButton = document.createTextNode("Remove");
	button.appendChild(textForButton);
	div.appendChild(button);

	holder.appendChild(div);
	numberOfIngredients ++;
	setNumberOfIngredients();
}

function removeIngredient(id) {
	// Div
	var div = document.getElementById("ingredient-div-" + id);
	div.remove();

	// Change ids of remaining elements
	changeIds(id);
}

function changeIds(id) {
	id = parseInt(id);
	for(var i = id + 1; i < numberOfIngredients; i++) {
		// Div
		document.getElementById("ingredient-div-" + i).setAttribute("id", "ingredient-div-" + (i - 1));

		// Name
		document.getElementById("ingredient-name-" + i).setAttribute("id", "ingredient-name-" + (i - 1));
		document.getElementById("ingredient-name-" + (i - 1)).setAttribute("name", "ingredient-name-" + (i - 1));

		// Quantity
		document.getElementById("ingredient-quantity-" + i).setAttribute("id", "ingredient-quantity-" + (i - 1));
		document.getElementById("ingredient-quantity-" + (i - 1)).setAttribute("name", "ingredient-quantity-" + (i - 1));

		// Unit
		document.getElementById("ingredient-unit-" + i).setAttribute("id", "ingredient-unit-" + (i - 1));
		document.getElementById("ingredient-unit-" + (i - 1)).setAttribute("name", "ingredient-unit-" + (i - 1));

		// Button
		document.getElementById("ingredient-button-" + i).setAttribute("id", "ingredient-button-" + (i - 1));
	}
	numberOfIngredients --;
	setNumberOfIngredients();
}

setNumberOfIngredients();
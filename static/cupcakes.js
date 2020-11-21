'use strict'

/**
 * Adds a single cupcake to the list
 * @param {*} flavor Flavor of cupcake
 * @param {*} size Size of cupcake
 * @param {*} rating Rating of cupcake
 * @param {*} image Image of cupcake
 * @param {*} list List to add cupcake to
 */
let createLiCupcake = (flavor, size, rating, image, list) => {
    let li = document.createElement("li");
    let img = document.createElement("img");

    li.innerText = ` ${size} ${flavor} cupcake rated ${rating}/10`;
    img.src = image;
    img.alt = "Cupcake"

    li.prepend(img)
    list.append(li)
}

/**
 * Grabs a list of cupcakes and updates the page with them
 * @param {*} list The list to add all cupcakes
 */
let getCupcakes = async list => {
    let cupcakes = await axios.get('http://localhost:5000/api/cupcakes');
    for (let cupcake of cupcakes.data.cupcakes) {
        createLiCupcake(cupcake.flavor, cupcake.size, cupcake.rating, cupcake.image, list)
    }
};

/**
 * Creates a new cupcake and posts it to the database and adds the new cupcake to the list
 * @param {*} flavor Flavor of cupcake
 * @param {*} size Size of cupcake
 * @param {*} rating Rating of cupcake
 * @param {*} image Image of cupcake
 * @param {*} list List to add cupcake to
 */
let createCupcake = async (flavor, size, rating, image, list) => {
    let newCupcake
    let newCupcakeData = {
        flavor: flavor.value,
        size: size.value,
        rating: rating.value
    };
    if (image.value != null && image.value.length != 0) {
        newCupcakeData.image = image.value
    }
    newCupcake = await axios.post('http://localhost:5000/api/cupcakes', newCupcakeData);
    newCupcake = newCupcake.data.cupcake

    createLiCupcake(newCupcake.flavor, newCupcake.size, newCupcake.rating, newCupcake.image, list);

    //Clear form
    flavor.value = null;
    size.value = null;
    rating.value = null;
    image.value = null;
}

document.addEventListener("DOMContentLoaded", () => {
    let cupcakes = document.querySelector("#cupcakes");
    let newCupcakeForm = document.querySelector("#newCupcake");
    let flavor = document.querySelector("#flavor");
    let size = document.querySelector("#size");
    let rating = document.querySelector("#rating")
    let image = document.querySelector("#image")

    newCupcakeForm.addEventListener("submit", event => {
        event.preventDefault();

        createCupcake(flavor, size, rating, image, cupcakes)
    });

    getCupcakes(cupcakes);
});
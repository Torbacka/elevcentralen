document.body.style.border = "5px solid yellow";
const teachers = [...document.getElementsByClassName("list-group teachers")[0].getElementsByTagName("label")];

var newItem = document.createElement("LI");       // Create a <li> node
var textnode = document.createTextNode("Water");  // Create a text node
newItem.appendChild(textnode);
document.getElementsByClassName("tab-content transparent")[0].insertBefore(newItem, document.getElementsByClassName("tab-content transparent")[0].childNodes[0]);


teachers.forEach(label =>{
    console.log(label.getAttribute("data-name"));
});

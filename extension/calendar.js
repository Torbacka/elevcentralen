document.body.style.border = "5px solid yellow";
const teachers = [...document.getElementsByClassName("list-group teachers")[0].getElementsByTagName("label")];


teachers.forEach(label =>{
    console.log(label.getAttribute("data-name"));
});

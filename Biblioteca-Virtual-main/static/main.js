console.log("JS conectado!")

function searchbar() {

    let input = document
        .querySelector('.search-txt')
        .value
        .toLowerCase()

    let livros = document.querySelectorAll('.livro')

    livros.forEach(livro => {

        let titulo = livro
            .querySelector('h2')
            .innerText
            .toLowerCase()

        if (titulo.includes(input)) {
            livro.style.display = "block"
        }
        else {
            livro.style.display = "none"
        }
    })
}
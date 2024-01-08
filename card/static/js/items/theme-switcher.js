const chk = document.getElementById('chk');
const mainDiv = document.getElementById('main');
const nav = document.querySelector('nav');

chk.addEventListener('change', () => {
    // Altera a classe 'dark' para o corpo do documento
    document.body.classList.toggle('dark');

    // Pega todos os elementos filhos da div principal
    const children = mainDiv.querySelectorAll('*');
    
    // Altera a classe 'dark' para cada elemento filho
    children.forEach(child => {
        child.classList.toggle('dark');
    });
    
    // Inverte as classes 'dark' e 'lite' no elemento <nav>
    nav.classList.toggle('dark');
    nav.classList.toggle('lite');
});

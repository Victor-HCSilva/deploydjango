console.log('⚠️⚠️⚠️ Apenas funcionários, medicos🔧! ⚠️⚠️⚠️')

function formatarCPF(cpf) {
    // Remove caracteres não numéricos
    cpf = cpf.replace(/[^0-9]/g, '');
    
    // Verifica se o CPF tem 11 dígitos
    if (cpf.length !== 11) {
    return cpf; // Retorna o CPF sem formatação se não tiver 11 dígitos
    }
    
    // Formata o CPF: xxx.xxx.xxx-xx
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
    
    // Exemplo de uso:
    const inputCPF = document.querySelector("body > div.container > form > div.row > div.col-md-4 > input")
    const inputCPF_Search = document.querySelector("#id_cpf")
    
    inputCPF.addEventListener('input', function() {
    this.value = formatarCPF(this.value);
    
});
    inputCPF_Search.addEventListener('input', function() {
    this.value = formatarCPF(this.value);
    });

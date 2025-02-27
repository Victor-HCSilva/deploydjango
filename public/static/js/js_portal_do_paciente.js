console.log('teste');

function calcularIMC() {
  const peso = parseFloat(document.getElementById('peso').value);
  const altura = parseFloat(document.getElementById('altura').value);

  if (isNaN(peso) || isNaN(altura) || peso <= 0 || altura <= 0) {
    document.getElementById('resultado').textContent = "Por favor, insira valores válidos para peso e altura.";
    return;
  }

  const imc = peso / (altura * altura);
  let mensagem = "Seu IMC é: " + imc.toFixed(2) + " - ";
  if (peso >= 1 && altura > 0.2 ){
    if (imc < 18.5) {
      mensagem += "Abaixo do peso.";
    } else if (imc >= 18.5 && imc < 25) {
      mensagem += "Peso normal.";
    } else if (imc >= 25 && imc < 30) {
      mensagem += "Sobrepeso.";
    } else if (imc >= 30 && imc < 35) {
      mensagem += "Obesidade grau I.";
    } else if (imc >= 35 && imc < 40) {
      mensagem += "Obesidade grau II (severa).";
    } else {
      mensagem += "Obesidade grau III (mórbida).";
    }  
  } else {
    mensagem += "Inválido.";
  }

  document.getElementById('resultado').textContent = mensagem;
}



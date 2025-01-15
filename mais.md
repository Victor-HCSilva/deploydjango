- imagem
 `python  manage.py graph_models -a -o output.png`
 - https://youtu.be/8z3osE4aJ0I?feature=shared

 Você pode forçar um `git pull` sobrescrevendo suas alterações locais usando a opção `--force` com o comando `git reset`. No entanto, **essa é uma operação perigosa e deve ser usada com extrema cautela**, pois você perderá qualquer alteração local que não tenha sido commitada.

**Recomendação:** Antes de usar qualquer comando forçado, é altamente recomendável criar um backup do seu trabalho local ou commitar e fazer o push de suas mudanças para um branch separado. Isso garantirá que você não perca nada importante.

**Passos para um `git pull` forçado (com precaução):**

1. **(Altamente Recomendado) Salve suas alterações locais:**
   * **Crie um backup:** Copie sua pasta de trabalho para outro local.
   * **Commit e push para um branch temporário:** Se você deseja manter suas alterações, use:
     ```bash
     git add .
     git commit -m "Backup das alterações antes do pull forçado"
     git checkout -b backup-branch
     git push origin backup-branch
     ```

2. **Descarte as alterações locais:**
   * Use o comando `git reset --hard`:
     ```bash
     git reset --hard origin/main  # Substitua 'main' pelo nome do seu branch remoto
     ```
     Isso irá descartar todas as suas alterações locais e fará com que seu branch local seja idêntico ao branch remoto.

3. **Faça o pull do repositório:**
   * Agora você pode fazer o pull normalmente, sem conflitos:
     ```bash
     git pull
     ```

**Explicação dos comandos:**

* `git reset --hard origin/main`:
    * `git reset`: É um comando usado para desfazer alterações no Git.
    * `--hard`:  Essa opção descarta *todas* as alterações locais (arquivos não commitados, alterações no staging e commits locais).
    * `origin/main`: Refere-se ao branch `main` do repositório remoto `origin`.

* `git pull`: Baixa as alterações mais recentes do branch remoto e as mescla no seu branch local.

**Exemplo completo com o backup recomendado:**

```bash
# 1. Salvar as alterações locais (opcional, mas altamente recomendado):
git add .
git commit -m "Backup antes do pull forçado"
git checkout -b backup-branch
git push origin backup-branch

# 2. Descartar as alterações locais e sincronizar com o branch remoto:
git reset --hard origin/main 

# 3. Fazer o pull:
git pull

# Se precisar recuperar seu trabalho anterior, troque para o branch de backup
# git checkout backup-branch 
```

**Atenção:**

* **Perda de dados:** Lembre-se que o comando `git reset --hard` é **irreversível** e pode resultar na perda de dados se você não tiver um backup.
* **Conflitos:** Embora isso force a sincronização, pode ser que você tenha que resolver conflitos posteriormente, caso outros desenvolvedores também tenham feito alterações no mesmo arquivo.
* **Use com responsabilidade:** Utilize essa abordagem apenas quando realmente necessário e quando você tiver certeza de que compreende os riscos.

**Alternativa ao `reset --hard` (mais segura):**

Em vez de usar o `git reset --hard`, você pode optar por:

1. **Fazer stash das alterações:**
   ```bash
   git stash
   ```
2. **Fazer o pull:**
   ```bash
   git pull
   ```
3. **Aplicar as alterações stashed (e resolver conflitos se houver):**
   ```bash
   git stash pop
   ```

Essa abordagem é mais segura porque permite que você salve suas alterações locais em um "stash" temporário e as aplique depois do pull, dando a você a chance de lidar com conflitos de maneira mais controlada.

**Conclusão:**

Usar `git pull` forçando todas as alterações deve ser a última opção. É muito mais seguro fazer backup de seu trabalho ou criar um stash antes de qualquer ação que possa sobrescrever seu código. Se você ainda não tem certeza do que está fazendo, é melhor pedir ajuda a um colega mais experiente para evitar perder seu trabalho.


# deploy

```
pip install --user pythonanywhere
```
```pa_autoconfigure_django.py https://github.com/user-name/repositorio.git --python=3.10
```



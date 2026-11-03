# Exercício Selenium — Login com E-mail incorreto e Registrar Usuário

> Item postado: 28 de set. (editado: 28 de set.)
> Não entregue

**Atenção:** esse exercício será usado como pré-requisito para outra atividade adiante

## Descrição

Criar teste end-to-end com selenium para a funcionalidade Login com E-mail incorreto e Registrar Usuário do site https://automationexercise.com/. O cenário é o mesmo do Test Case 3 e 1, do link Test Cases (replicados abaixo).

## Entrega

A atividade deverá ser entregue em um repositório público. Enviar link nesse ativiade

## Critérios de teste

Usar os critérios de particionamento de classes de equivalência e análise de valor limite para pensar em casos de teste. Considerar ao menos 5 entradas.

## Test Case 3: Login User with incorrect email and password

1. Launch browser
2. Navigate to url 'http://automationexercise.com
3. Verify that home page is visible successfully
4. Click on 'Signup / Login' button
5. Verify 'Login to your account' is visible
6. Enter incorrect email address and password
7. Click 'login' button
8. Verify error 'Your email or password is incorrect!' is visible

## Caso de Teste - Registrar Usuário

## Test Case 1: Register User

1. Launch browser
2. Navigate to url 'http://automationexercise.com&#39;
3. Verify that home page is visible successfully
4. Click on 'Signup / Login' button
5. Verify 'New User Signup!' is visible
6. Enter name and email address
7. Click 'Signup' button
8. Verify that 'ENTER ACCOUNT INFORMATION' is visible
9. Fill details: Title, Name, Email, Password, Date of birth
10. Select checkbox 'Sign up for our newsletter!'
11. Select checkbox 'Receive special offers from our partners!'
12. Fill details: First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number
13. Click 'Create Account button'
14. Verify that 'ACCOUNT CREATED!' is visible
15. Click 'Continue' button
16. Verify that 'Logged in as username' is visible
17. Click 'Delete Account' button
18. Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button

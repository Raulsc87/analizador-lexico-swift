import Foundation

let nombreUniversidad = "Universidad Mesoamericana"
let nombreCurso = "Compiladores"
let anioActual = 2026

var estudiante = "Raul Soto"
var edad = 21
var promedio = 85.5
var activo = true
var eliminado = false

let notaMinima = 61
let cantidadCursos = 5

func mostrarSaludo(nombre: String) {
    print("Hola \(nombre)")
}

func sumar(a: Int, b: Int) -> Int {
    return a + b
}

func calcularPromedio(nota1: Double, nota2: Double) -> Double {
    let resultado = (nota1 + nota2) / 2.0
    return resultado
}

struct Curso {
    var nombre: String
    var nota: Double
    var aprobado: Bool
}

class Persona {
    var nombre: String
    var edad: Int

    init(nombre: String, edad: Int) {
        self.nombre = nombre
        self.edad = edad
    }

    func mostrarDatos() {
        print(nombre)
        print(edad)
    }
}

let curso1 = Curso(
    nombre: "Compiladores",
    nota: 90.0,
    aprobado: true
)

let persona1 = Persona(
    nombre: "Raul",
    edad: 21
)

mostrarSaludo(nombre: estudiante)

let resultadoSuma = sumar(
    a: 10,
    b: 20
)

let nuevoPromedio = calcularPromedio(
    nota1: 80.5,
    nota2: 90.5
)

if edad >= 18 {
    print("Es mayor de edad")
} else {
    print("Es menor de edad")
}

if promedio >= 90.0 && activo == true {
    print("Excelente rendimiento")
} else if promedio >= 61.0 {
    print("Curso aprobado")
} else {
    print("Curso reprobado")
}

if eliminado == false {
    print("El usuario está disponible")
}

var contador = 0

while contador < 5 {
    print(contador)
    contador += 1
}

for numero in 1...5 {
    print(numero)
}

let numeros = [10, 20, 30, 40, 50]

for numero in numeros {
    print(numero)
}

var total = 0

for numero in numeros {
    total = total + numero
}

switch edad {
case 0:
    print("Edad inválida")
case 1...17:
    print("Menor de edad")
case 18...60:
    print("Adulto")
default:
    print("Adulto mayor")
}

var puntos = 100
puntos += 20
puntos -= 10
puntos *= 2
puntos /= 5

let residuo = puntos % 3
let esIgual = puntos == 44
let esDiferente = puntos != 50
let esMayor = puntos > 10
let esMenor = puntos < 100
let esMayorIgual = puntos >= 44
let esMenorIgual = puntos <= 44
let condicionAnd = activo && !eliminado
let condicionOr = activo || eliminado

print(nombreUniversidad)
print(nombreCurso)
print(anioActual)
print(cantidadCursos)
print(notaMinima)
print(resultadoSuma)
print(nuevoPromedio)
print(curso1.nombre)
print(curso1.nota)
print(curso1.aprobado)

persona1.mostrarDatos()

if esIgual {
    print("El valor es igual")
}

if esDiferente {
    print("El valor es diferente")
}

if condicionAnd {
    print("La condición AND es verdadera")
}

if condicionOr {
    print("La condición OR es verdadera")
}

print("Fin del programa")
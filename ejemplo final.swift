import Foundation
var nombre: String = "Diego"
var edad: Int = 20
var altura: Double = 1.75
var activo: Bool = true
let universidad: String = "Mesoamericana"
let semestre: Int = 6
var promedio: Double = 85.5
var aprobado: Bool = false
print(nombre)
print(edad)
print(altura)
if edad >= 18 {
    aprobado = true
} else {
    aprobado = false
}
if aprobado == true && promedio >= 61.0 {
    print("Aprobado")
} else {
    print("Reprobado")
}
for numero in 1...5 {
    print(numero)
}
var contador: Int = 0
while contador < 10 {
    contador += 1
}
func saludar(nombre: String) -> String {
    return "Hola " + nombre
}
let mensaje: String = saludar(nombre: nombre)
print(mensaje)
struct Estudiante {
    var nombre: String
    var edad: Int
    var nota: Double
}
var estudiante = Estudiante(nombre: "Carlos", edad: 21, nota: 90.0)
print(estudiante.nombre)
print(estudiante.edad)
class Curso {
    var nombre: String
    var creditos: Int
    init(nombre: String, creditos: Int) {
        self.nombre = nombre
        self.creditos = creditos
    }
}
var curso = Curso(nombre: "Programacion", creditos: 4)
print(curso.nombre)
switch semestre {
case 1:
    print("Primer semestre")
case 2:
    print("Segundo semestre")
case 3:
    print("Tercer semestre")
default:
    print("Otro semestre")
}
var suma: Int = 10 + 20
var resta: Int = 50 - 15
var multiplicacion: Int = 5 * 4
var division: Int = 100 / 5
var modulo: Int = 10 % 3
var resultado: Bool = suma > resta
resultado = suma != resta
resultado = suma <= resta
resultado = suma >= resta
resultado = activo || aprobado
resultado = activo && aprobado
resultado = !aprobado
edad += 1
promedio -= 2.5
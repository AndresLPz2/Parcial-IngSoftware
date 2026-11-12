# Registro de cambios

Formato de registro de cambios; versiones según el esquema semántico.

## [2.1.0] - 2026-11-11
### Agregado
- Cliente empresarial con 12% de descuento.
- Exención del recargo de zona empresarial cuando peso > 10 kg.
### Corregido
- Validación personalizada de peso, zona, día, cliente y cupón.
- Recargo de fin de semana para sábado y domingo, posterior a descuentos.
- Descuentos según B, cupón desconocido según F, piso y redondeo de mitades hacia arriba.
### Cambiado
- Reorganización por estrategias de zona, funciones separadas y constantes con nombre.
- La función ofrece `calc(peso, zona, cliente, dia, cupon=None)` sin salida a consola.
### Pruebas
- 32 pruebas aprobadas; cobertura combinada medida de 100%.

## [2.0.0] - 2026-11-11
### Corregido
- Peso máximo personalizado, validaciones de zona/día/cliente, fin de semana y cupón.
- Redondeo de mitades hacia arriba y orden del recargo después de descuentos.
### Cambiado
- Eliminado `flag`, cambio incompatible de interfaz principal.

## [1.0.0] - 2026-11-11
### Agregado
- Versión heredada de `calc` descrita en el PDF. Etiquetar solo el registro de la copia original.

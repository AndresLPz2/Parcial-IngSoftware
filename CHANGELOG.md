# Changelog

Formato Keep a Changelog; versiones según SemVer.

## [2.1.0] - 2026-11-11
### Added
- Cliente empresarial con 12% de descuento.
- Exención del recargo de zona empresarial cuando peso > 10 kg.
### Fixed
- Validación personalizada de peso, zona, día, cliente y cupón.
- Recargo de fin de semana para sábado y domingo, posterior a descuentos.
- Descuentos según B, cupón desconocido según F, piso y redondeo half-up.
### Changed
- Refactor por estrategias de zona, funciones extraídas y constantes nombradas.
- La API ofrece `calc(weight, zone, customer, day, coupon=None)` sin salida a consola.
### Tests
- 32 pruebas aprobadas; cobertura combinada medida de 100%.

## [2.0.0] - 2026-11-11
### Fixed
- Peso máximo personalizado, validaciones de zona/día/cliente, fin de semana y cupón.
- Redondeo half-up y orden del recargo después de descuentos.
### Changed
- Eliminado `flag`, cambio incompatible de interfaz (major).

## [1.0.0] - 2026-11-11
### Added
- Versión heredada de `calc` descrita en el PDF. Etiquetar solo el commit de la copia original.

# Linkding para la evaluación de calidad

Este repositorio es una copia derivada de [Linkding](https://github.com/sissbruecker/linkding),
creado por sus autores originales y distribuido bajo la licencia MIT conservada en
`LICENSE.txt`. La evaluación corresponde a la versión 1.47.0, commit original
`24b5ad6cc9bde497b5d1b1e86aed5a2fb7d25c2f`.

La rama `evaluacion-render-gratuito` agrega configuración de alojamiento para el
trabajo académico. No introduce cambios funcionales en el gestor de marcadores.
La imagen se fija por versión y digest para mantener el producto evaluado.

## Alojamiento sin pago

- Render Free ejecuta la aplicación y proporciona una dirección HTTPS.
- Neon Free conserva cuentas, marcadores, notas y etiquetas en PostgreSQL.
- `render.yaml` declara únicamente un servicio gratuito. No crea discos ni bases
  de datos de pago en Render.
- No es necesario contratar un dominio para usar la dirección de Render.

Hay límites de uso. Render suspende la instancia tras 15 minutos sin visitas y
la siguiente apertura puede tardar alrededor de un minuto. Los planes gratuitos
pueden suspender el servicio al consumir sus cuotas. No se activan planes de pago
ni actualizaciones automáticas con esta configuración.

## Activación

1. Crear una cuenta gratuita en Neon y un proyecto PostgreSQL de uso exclusivo
   para esta demostración. Elegir una región de Estados Unidos cercana a Oregon
   cuando esté disponible.
2. Obtener la cadena de conexión PostgreSQL del proyecto, con `sslmode=require`.
   No publicarla en GitHub ni en el informe.
3. En Render, crear un Blueprint desde este repositorio, seleccionando la rama
   `evaluacion-render-gratuito` y el archivo `render.yaml`.
4. Verificar que el servicio indique **Free / $0**. Proporcionar `DATABASE_URL`
   como variable secreta. Render genera la clave de sesión y la contraseña de
   `evaluador`; se conservan como variables de entorno de la cuenta.
5. Desplegar y verificar `/health` y el inicio de sesión. La contraseña inicial
   puede consultarse en la variable `LD_SUPERUSER_PASSWORD` de Render.
6. Crear una cuenta normal para la demostración del profesor mediante el panel
   de administración. Compartir su acceso por un canal privado.

## Qué conserva y qué limita

Los datos relacionales viven en Neon. Se desactivan capturas de páginas, cargas de
archivos y tareas en segundo plano porque el disco gratuito de Render es efímero.
No se incluyen las cuentas, contraseñas, tokens, documentos del curso, audio ni
base SQLite del laboratorio local. La instalación online comienza con datos nuevos.

## Comprobar antes de presentarlo

Después de activar el alojamiento, crear y consultar un marcador, probar búsqueda,
etiquetas e intercambio y comprobar que sus datos permanecen después de un reinicio.
Registrar la URL pública, el proveedor y la configuración PostgreSQL en una nueva
campaña de evidencias. Los tiempos medidos previamente en localhost siguen
correspondiendo a ese entorno y no deben atribuirse al servidor online.

La configuración se ha comprobado estáticamente y contra el cargador de ajustes
de Django. La validación del contenedor y la conexión real con Neon se completan
en el primer despliegue; no se afirma que exista una URL online antes de esa prueba.

## Referencias

- [Instalación oficial de Linkding](https://linkding.link/installation/)
- [Opciones de Linkding](https://linkding.link/options/)
- [Servicios gratuitos de Render](https://render.com/docs/free)
- [Blueprints de Render](https://render.com/docs/blueprint-spec)
- [Plan gratuito de Neon](https://neon.com/pricing)

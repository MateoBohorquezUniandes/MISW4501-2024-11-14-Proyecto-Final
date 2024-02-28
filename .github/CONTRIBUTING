## Tabla de Contenidos


## Git Branches

Los repositorios deben usar la rama `main` como rama principal.
Esta rama debe estar "protegida" en GitHub y requerir revisiones de relaciones públicas y comprobaciones de estado antes de fusionarse. consulte [configuración de la rama de GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule)

Las adiciones a la rama `main` deben seguir estos conceptos simples:

- Utilice ramas `feat` para todas las funciones nuevas.
- Utilice ramas `fix` para correcciones de errores.
- Utilice ramas `chore` para cambios que no sean correcciones ni nuevas funcionalidades
- Utilice ramas `release` para creación de releases
- Realizar **Pull Requests** para fusionar ramas `feat`, `fix`, `chore` y `relsease` con la rama `main`.
- Mantener la rama `main` actualizada y con alta calidad.


## Mensajes de los Commits

Un commit:

- Idealmente debería abordar un problema
- debería ser un cambio autónomo en la base del código
- no debe agrupar cambios no relacionados

Los repositorios deben seguir la siguiente convención (cuando sea posible):

```md
<TIPO>(<PALABRA_CLAVE>): <DESCRIPCION>

<DETALLE>
```

### <TIPO>

El `<TIPO>` dentro del commit indica qué tipo de cambiofue realizado. Este valor debe ser alguno de los siguientes valores:

- `feat`: Indica que el cambio corresponde a una nueva funcionalidad
- `fix`: indica que el cambio corresponde a una corrección
- `chore` Indica que el cambio corresponde a tareas que no son `feat` ni `fix`. Usualmente, son tareas del release

### <PALABRA_CLAVE>

La `<PALABRA_CLAVE>` debe indicar de manera precisa cuál fue el lugar (código, flujo, historia de usuario) en donde se realizó el cambio.

### <DESCRIPCION>

La `<DESCRIPCION>` debe ser un mensaje de no mas de 72 caracteres en donde se resumen los cambios realizados.

### <DETALLE>

El `<DETALLE>` hace referencia a un texto explicativo más detallado, en caso de ser necesario necesario.
La línea en blanco que separa el resumen del cuerpo es crítico (a menos que omita el cuerpo por completo); varias herramientas como `log`, `shortlog` y `rebase` pueden confundirse si los ejecutas juntos.

Explique el problema que este compromiso está resolviendo. Concéntrate en por qué debes hacer este cambio en lugar de cómo (el código lo explica). Son ¿Hay efectos secundarios u otras consecuencias no intuitivas de este cambio? Este es el lugar para explicárselos a otra persona que lea su mensaje en el futuro.

### Ejemplo 

```md
feat(CI): creación de workflows

Se crean los workflows para la ejecución de pruebas de regresión mediante el uso de Github Actions.
```

```md
fix(compose): modificación de puertos para api

Se corrigen los puersto del microservio X para evitar colisiones con otros servicios
```

## Creación de Pull Request

Los Pull Requests deben ser dirigidos a la rama `main` de manera continua. Se deben seguir las siguientes pautas:

- El título del Pull Request debe seguir el formato definido en la sección [**Mensajes de los Commits**](/#Mensajes-de-los-Commits).
- El Pull request debe utilizar el formato del archivo `pull_request_template.md`. Toda la inforamción debe estar diligenciada
- Se deben colocar los labels necesarios
- Se debe colocar el Milestone correspondiente

Por lo general, los R también deberían intentar responder a uno o más problemas abiertos. Puede vincular una solicitud de extracción a un problema para mostrar que hay una solución en progreso y cerrar automáticamente el problema cuando se fusiona la solicitud de extracción; consulte [Vincular una solicitud de extracción a un problema](https://docs.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue).


### Pull Request Listo para revisión

- Si su solicitud de extracción aún no está lista para fusionarse, ábrala como **borrador**.
Más información sobre cómo hacer esto está [disponible en la documentación de GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests).
Esto le indica al equipo de desarrollo que la solicitud de extracción es un "trabajo en progreso" y que planea continuar trabajando en ella.

- Cuando su solicitud de extracción esté **"Listo para revisión"**, puede seleccionar esta opción en la página del RP, que notificará a los mantenedores del proyecto para que revisen los cambios propuestos.

## Pull Request Reviews

### Fuentes

- https://github.com/aiidateam/aiida-core/wiki/Best-practises-for-code-review
- https://google.github.io/eng-practices/review/reviewer/standard.html
- https://www.ibm.com/developerworks/rational/library/11-proven-practices-for-peer-review/index.html
- https://phauer.com/2018/code-review-guidelines/

[eng-practises]: https://google.github.io/eng-practices/review/reviewer/standard.html
[cisco-study]: https://www.ibm.com/developerworks/rational/library/11-proven-practices-for-peer-review/index.html
[phauer]: https://phauer.com/2018/code-review-guidelines/


### Estándares

#### Aprobar cambios

- Los hechos y datos técnicos prevalecen sobre las preferencias personales.
- Favorecer la aprobación de un PR una vez que definitivamente mejore la salud general del código, incluso si no es perfecto

#### Vigilancia

- Ser receptivo a las solicitudes de revisión.
    Los usuarios que se esfuerzan por contribuir son los que más merecen nuestra atención, y la revisión oportuna de las relaciones públicas es un gran motivador.
- Mira cada línea de código que se está modificando.
- Utilice una lista de verificación como la siguiente, especialmente si es nuevo en la revisión de códigos.

#### Comunicación

- Ofrecer ánimo por las cosas bien hechas, no señalar únicamente los errores.
- Está bien mencionar lo que podría mejorarse, pero no es obligatorio ( anteponga a dichos comentarios "Nit:" para "quisquilloso")
- Es bueno compartir conocimientos que ayuden al remitente a mejorar su comprensión del código (aclare dónde espera o no espera acción)

### Lista de verificación: qué buscar

#### Alcance

- ¿Le piden que revise más de 200 líneas de código?
    Entonces no dude en pedirle al remitente que divida las relaciones públicas: la efectividad de la revisión [cae sustancialmente más allá de las 200 líneas de código] [estudio de Cisco].
- ¿Hay partes del código base que no se han modificado, pero *deberían* adaptarse a los cambios?
    ¿El cambio de código requiere una actualización de la documentación?

#### Diseño

- ¿Este cambio pertenece al código base?
- ¿Está bien integrado?

#### Funcionalidad

- ¿El código hace lo que pretendía el desarrollador?
- ¿Hay casos extremos en los que podría romperse?
- Para cambios en la interfaz de usuario: ¡pruébalo tú mismo! (difícil de entender leyendo el código)

#### Complejidad

- ¿Alguna línea, función o clase compleja que no sea fácil de entender?
- Sobreingeniería: ¿el código es demasiado complejo para el problema en cuestión?

#### Pruebas

- ¿Existen pruebas de nuevas funciones? ¿Los errores están cubiertos por una prueba que se interrumpe si el error reaparece?
- ¿Las pruebas son correctas y útiles? ¿Hacen afirmaciones simples y útiles?

#### Nombrar

- Un buen nombre es lo suficientemente largo para comunicar lo que hace el artículo, sin ser tan largo que resulte difícil de leer.

#### Comentarios

- ¿Los comentarios explican *por qué* existe el código (en lugar de *qué* está haciendo)?

#### Estilo y consistencia

- ¿La contribución sigue un estilo de codificación genérico (en su mayoría aplicado automáticamente)?




## Fusionar (Merge) Pull Requests


Hay tres formas de "fusionar" Pull Request en GitHub. **Aplastar y fusionar** es el método preferido, aplicable a la mayoría de los RP, pero hay algunos casos de uso en los que se aplican los otros dos:

- **Squash And Merge**: tomar todas las confirmaciones, aplastarlas en una sola y colocarla encima de la rama base.
   - Elija esto de forma predeterminada para solicitudes de extracción que aborden un único problema y estén bien representadas por una única confirmación.
   - La persona que fusiona el PR debe elegir un mensaje de confirmación claro al fusionar (a través de la interfaz de usuario de GitHub)

- **Rebase y fusión**: toma todas las confirmaciones y 'recrealas' encima de la rama base. Todas las confirmaciones se recrearán con nuevos hashes.
   - Elija esto para solicitudes de extracción que requieran más de una confirmación.
   - Asegúrese de que [las confirmaciones tengan mensajes de confirmación claros] (dev/commits).
   - Ejemplos: RP que contienen múltiples confirmaciones con cambios individualmente significativos; RP que tienen confirmaciones de diferentes autores (aplastar las confirmaciones eliminaría la atribución)

- **Fusionar con confirmación de fusión**: coloque todas las confirmaciones tal como están en la rama base, con una confirmación de fusión en la parte superior
   - Elija relaciones públicas colaborativas con muchos compromisos.
      Aquí, el compromiso de fusión proporciona beneficios reales.

Una desventaja de la fusión de squash es que combina múltiples confirmaciones en una sola. Esto suele estar bien, ya que los RP tienen muchas confirmaciones como "corregir errores tipográficos" y "abordar comentarios". Agruparlos en un solo mensaje permite que la fusión de relaciones públicas cree [un mensaje de confirmación que sea claro y conciso] (dev/commits). Sin embargo, a veces un PR está mejor representado por *múltiples* confirmaciones. En este caso, está bien rebase-merge o fusion-commit.

> **¿Cómo puedo cambiar el nombre de mis confirmaciones localmente?**
>
> Si desea cambiar el nombre de las confirmaciones localmente (por ejemplo, si desea realizar una confirmación de rebase en GitHub, pero primero desea limpiar el historial de confirmaciones para usar [mensajes de confirmación que sean claros y concisos](dev/ confirma)), puedes probar una [**rebase interactiva**]( https://thinkbot.com/blog/git-interactive-rebase-squash-amend-rewriting-history).
> Esto le permite convertir una serie de confirmaciones en una cantidad menor de confirmaciones y puede elegir el mensaje de confirmación para cada una.
> Sin embargo, esta es una técnica avanzada de git, ¡así que solo haz esto si sabes lo que estás haciendo! Si solo desea fusionar sus confirmaciones sin realizar un cambio de base interactivo, no es el fin del mundo.


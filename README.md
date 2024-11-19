# py-up-data-mining
Este repositorio contiene el código, datos y análisis del estudio:  
**"Impacto de Condiciones de Vivienda y Factores Socioeconómicos en la Mortalidad por Enfermedades Respiratorias en Perú (2022)"**.

El objetivo del análisis es explorar y comprender cómo las condiciones de vivienda, factores demográficos, socioeconómicos y climáticos influyen en la mortalidad por enfermedades respiratorias en el Perú. Para ello, se aplicaron técnicas avanzadas de **Data Mining**, como análisis exploratorio, reglas de asociación y modelamiento predictivo, para identificar patrones clave.

---
## Contenido del Repositorio
```plaintext
📦 py-up-data-mining
├── 📁 data                                # Archivos de datos originales y procesados
│   ├── raw/                          # Datos originales (CSV)
│   │   ├── enaho_salud.csv                # Datos de salud (ENAHO)
│   │   ├── enaho_vivienda.csv             # Datos de vivienda (ENAHO)
│   │   ├── fallecidos_sinadef.csv         # Datos de fallecidos (SINADEF) **
│   │   ├── variables_meteorologicas.csv   # Datos meteorológicos (SENAMHI) **
│   │   ├── etiquetas_sinadef.csv          # Etiquetas adicionales (SINADEF)
│   │   ├── ubigeos.csv                    # Tabla de ubigeos
│   ├── processed/                         # Datos procesados
│       ├── processed_data.xlsx            # Output preprocesado para análisis
├── 📁 notebooks                           # Notebooks Jupyter para cada etapa
│   ├── preprocessing.ipynb                # Notebook para preprocesamiento
│   ├── association_rules.ipynb            # Notebook para reglas de asociación
│   ├── predictive_model.ipynb             # Notebook para modelo predictivo
├── 📁 docs                                # Documentos relacionados con el proyecto
│   ├── proyecto.pdf                       # Documento del proyecto
├── 📄 README.md                           # Descripción del repositorio
```
**Nota**: Los archivos marcados con ** (fallecidos_sinadef.csv y variables_meteorologicas.csv) deben descargarse debido a su tamaño: [click aquí](https://drive.google.com/drive/folders/16JAKMwNGBhFpue7HpaAQel7czkgZjKmN?usp=sharing)
---
## Metodología
Se utilizó la metodología **Knowledge Discovery in Databases (KDD)**, que consta de las siguientes fases:
1. **Entendimiento del problema**: Definición de las variables clave relacionadas con enfermedades respiratorias.
2. **Selección y recopilación de datos**: Integración de datos de SINADEF, ENAHO y SENAMHI.
3. **Limpieza y preprocesamiento**: Imputación de valores nulos, codificación de variables categóricas y reducción de dimensionalidad.
4. **Análisis exploratorio**: Identificación de correlaciones y patrones iniciales.
5. **Modelamiento**: Aplicación de reglas de asociación y modelos predictivos.
---
## Resultados Destacados
* Identificación de asociaciones entre factores climáticos (e.g., bajas temperaturas) y mortalidad.
* Impacto de la calidad de vivienda y acceso a servicios básicos en el riesgo de enfermedades respiratorias.
* Patrones estacionales asociados a la incidencia de enfermedades respiratorias en regiones específicas del Perú.
---
## Integrantes del Equipo
* **Diego Antonio Saldaña Hidalgo**  
  Departamento de Ingeniería, Universidad del Pacífico.
* **Jhoan Leandro Vargas Collas**  
  Departamento de Ingeniería, Universidad del Pacífico.
* **Paulo Giusepe Verde Huayney**  
  Departamento de Ingeniería, Universidad del Pacífico.

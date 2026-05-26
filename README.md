# Lukning af IN aftaler i SAP

## Til brugere

Denne robot kan bruges lokalt til at lukke alle IN aftaler på en given FP og aftale.

Processen ser således ud:

1. Den givne FP åbnes i fmcacov.
2. Postlisten filtreres med den givne aftale.
3. For alle rækker i listen:
    1. Hvis RIM type ikke er 'IN' eller Aftalestatus er tom springes rækken over.
    2. Højreklik på Aftalestatus og tryk 'Vis aftale'.
    3. Klik Ændr og luk aftalen.

## For developers

This robot is made to be run from ITK Attended RPA.

When run the `main.py` file is run which will install uv and initialize a virtual environment to run the robot in.
Dependencies are defined in the `uv.lock` file.

The actual process of the robot is in `process.py`.

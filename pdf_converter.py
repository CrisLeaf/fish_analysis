import tabula

disembarkation_year = tabula.io.read_pdf("2011.pdf", pages="22")[0]
tabula.io.convert_into("2011.pdf", "data/disembarkation_year.csv", output_format="csv", pages="22")

frozen_production = tabula.io.read_pdf("2011.pdf", pages="26")[0]
tabula.io.convert_into("2011.pdf", "data/frozen_production.csv", output_format="csv", pages="26")

fresh_production = tabula.io.read_pdf("2011.pdf", pages="28")[0]
tabula.io.convert_into("2011.pdf", "data/fresh_production.csv", output_format="csv", pages="28")

prices = tabula.io.read_pdf("2011.pdf", pages="36")[0]
tabula.io.convert_into("2011.pdf", "data/prices.csv", output_format="csv", pages="36")
# Relatório mensal PDF – Apostolado da Oração
# Uso: Rscript relatorio_mensal.R [caminho.xlsx] [pasta_saida]

args <- commandArgs(trailingOnly = TRUE)
# Executar a partir da pasta apostolado_oracao:
#   Rscript r_scripts/relatorio_mensal.R
if (length(args) >= 1) {
  xlsx <- args[1]
} else {
  xlsx <- file.path("data", "apostolado.xlsx")
}
if (length(args) >= 2) {
  out_dir <- args[2]
} else {
  out_dir <- "relatorios"
}

if (!requireNamespace("ggplot2", quietly = TRUE)) {
  stop("Instale ggplot2: install.packages('ggplot2')")
}
if (!requireNamespace("readxl", quietly = TRUE)) {
  stop("Instale readxl: install.packages('readxl')")
}

library(ggplot2)
library(readxl)

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

membros <- read_excel(xlsx, sheet = "Membros")
mes <- format(Sys.Date(), "%Y-%m")
pdf_path <- file.path(out_dir, paste0("relatorio_", mes, ".pdf"))

sit_col <- if ("situacao" %in% names(membros)) "situacao" else names(membros)[13]
totais <- as.data.frame(table(membros[[sit_col]]))
names(totais) <- c("situacao", "quantidade")

p1 <- ggplot(totais, aes(x = reorder(situacao, -quantidade), y = quantidade, fill = situacao)) +
  geom_col(show.legend = FALSE) +
  labs(
    title = "Apostolado da Oração – Relatório Mensal",
    subtitle = paste("Paróquia São Jorge ·", format(Sys.Date(), "%d/%m/%Y")),
    x = "Situação",
    y = "Quantidade"
  ) +
  theme_minimal(base_size = 14) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

cons <- sum(tolower(as.character(membros$consagrada)) == "sim", na.rm = TRUE)
resumo <- data.frame(
  indicador = c("Total membros", "Consagrados"),
  valor = c(nrow(membros), cons)
)
p2 <- ggplot(resumo, aes(x = indicador, y = valor)) +
  geom_col(fill = "#6A1B9A") +
  labs(title = "Resumo geral") +
  theme_minimal(base_size = 14)

pdf(pdf_path, width = 11, height = 8.5)
print(p1)
print(p2)
dev.off()

cat("PDF gerado:", pdf_path, "\n")

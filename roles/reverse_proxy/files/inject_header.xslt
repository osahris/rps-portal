<?xml version="1.0"?>

<xsl:stylesheet version="1.1"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output
      method="html"
      version="5.0"
      doctype-system="about:legacy-compat"
      encoding="UTF-8"
      indent="yes" />

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="head">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
      <script type="application/javascript" src="/header.js" />
    </xsl:copy>
  </xsl:template>

  <xsl:template match="body">
    <xsl:copy>
      <nav id="rps-header"></nav>
      <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>

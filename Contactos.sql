USE [MARCOSDB]
GO

/****** Object:  Table [dbo].[Contactos]    Script Date: 08/18/2021 01:54:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Contactos](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Codigo] [nchar](10) NOT NULL,
	[Nombre] [nchar](50) NOT NULL,
	[Apellido] [nchar](50) NOT NULL,
	[Telefono] [nchar](20) NOT NULL,
	[Email] [nchar](50) NOT NULL,
 CONSTRAINT [PK_Contactos] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX  = ON, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 1) ON [PRIMARY]
) ON [PRIMARY]

GO



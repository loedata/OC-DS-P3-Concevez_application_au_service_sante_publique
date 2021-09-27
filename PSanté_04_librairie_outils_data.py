""" Librairie personnelle pour manipulation du dataframe,
    description des variables, renommage des colonnes...
"""

#! /usr/bin/env python3
# coding: utf-8

# ====================================================================
# Outils dataframe -  projet 3 Openclassrooms
# Version : 0.0.0 - CRE LR 21/02/2021
# ====================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import re

# --------------------------------------------------------------------
# -- VERSION
# --------------------------------------------------------------------
__version__ = '0.0.0'

# --------------------------------------------------------------------
# -- TYPES DES VARIABLES
# --------------------------------------------------------------------


def get_types_variables(df_work, types, type_par_var, graph):
    """ Permet un aperçu du type des variables
    Parameters
    ----------
    @param IN : df_work : dataframe, obligatoire
                types : Si True lance dtypes, obligatoire
                type_par_var : Si True affiche tableau des types de
                               chaque variable, obligatoire
                graph : Si True affiche pieplot de répartition des types
    @param OUT :None.
    """

    if types:
        # 1. Type des variables
        print("-------------------------------------------------------------")
        print("Type de variable pour chacune des variables\n")
        display(df_work.dtypes)

    if type_par_var:
        # 2. Compter les types de variables
        #print("Répartition des types de variable\n")
        values = df_work.dtypes.value_counts()
        nb_tot = values.sum()
        percentage = round((100 * values / nb_tot), 2)
        table = pd.concat([values, percentage], axis=1)
        table.columns = [
            'Nombre par type de variable',
            '% des types de variable']
        display(table[table['Nombre par type de variable'] != 0]
                .sort_values('% des types de variable', ascending=False)
                .style.background_gradient('seismic'))

    if graph:
        # 3. Schéma des types de variable
        # print("\n----------------------------------------------------------")
        #print("Répartition schématique des types de variable \n")
        # Répartition des types de variables
        df_work.dtypes.value_counts().plot.pie()
        plt.ylabel('')
        plt.show()

# ---------------------------------------------------------------------------
# -- VALEURS MANQUANTES
# ---------------------------------------------------------------------------

# Afficher des informations sur les valeurs manquantes


def get_missing_values(df_work, pourcentage, affiche_heatmap):
    """Indicateurs sur les variables manquantes
       @param in : df_work dataframe obligatoire
                   pourcentage : boolean si True affiche le nombre heatmap
                   affiche_heatmap : boolean si True affiche la heatmap
       @param out : none
    """

    # 1. Nombre de valeurs manquantes totales
    nb_nan_tot = df_work.isna().sum().sum()
    nb_donnees_tot = np.product(df_work.shape)
    pourc_nan_tot = round((nb_nan_tot / nb_donnees_tot) * 100, 2)
    print(
        f'Valeurs manquantes :{nb_nan_tot} NaN pour {nb_donnees_tot} données ({pourc_nan_tot} %)')

    if pourcentage:
        print("-------------------------------------------------------------")
        print("Nombre et pourcentage de valeurs manquantes par variable\n")
        # 2. Visualisation du nombre et du pourcentage de valeurs manquantes
        # par variable
        values = df_work.isnull().sum()
        percentage = 100 * values / len(df_work)
        table = pd.concat([values, percentage.round(2)], axis=1)
        table.columns = [
            'Nombres de valeurs manquantes',
            '% de valeurs manquantes']
        display(table[table['Nombres de valeurs manquantes'] != 0]
                .sort_values('% de valeurs manquantes', ascending=False)
                .style.background_gradient('seismic'))

    if affiche_heatmap:
        print("-------------------------------------------------------------")
        print("Heatmap de visualisation des valeurs manquantes")
        # 3. Heatmap de visualisation des valeurs manquantes
        plt.figure(figsize=(20, 10))
        sns.heatmap(df_work.isna(), cbar=False)
        plt.show()

# --------------------------------------------------------------------
# -- TRACE DES DIMENSIONS D'UN DATAFRAME
# --------------------------------------------------------------------
# Suivi des dimensions du jeu de données


def suivi_dimensions_dataframe(dataframe, df_traces, etape):
    """
    Affiche l'étape puis nombre de lignes et de variables pour le dataframe transmis
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT : dataframe de suivi des dimensions
    """
    # Taille : nombre de lignes/colonnes
    n_row, n_col = dataframe.shape
    print(f'Le jeu de données contient {n_row} lignes et {n_col} colonnes.')

    df_traces = df_traces.append({'Etape': etape, 'Nb_lignes': n_row,
                                  'Nb_variables': n_col}, ignore_index=True)

    # Suivi dimensions
    return df_traces

# --------------------------------------------------------------------
# -- DESCRIPTION DES VARIABLES
# --------------------------------------------------------------------


def description_variables(dataframe, type_var='all'):
    """
    Retourne la description des variables qualitatives/quantitatives
    ou toutes les variables du dataframe transmis :
    type, nombre de nan, % de nan et desc
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                type_var = 'all' ==> tous les types de variables
                           'cat' ==> variables catégorielles
                           'num' ==> variables quantitative
    @param OUT : dataframe de description des variables
    """
    df_taille = dataframe.shape[0]

    if type_var == 'num':
        desc_var = dataframe.describe()
    elif type_var == 'cat':
        desc_var = dataframe.describe(exclude=[np.number])
    else:
        desc_var = dataframe.describe(include='all')

    desc_type = pd.DataFrame(desc_var.dtypes, columns=['type']).T
    nb_nan = df_taille - desc_var.loc['count'].T
    pourcentage_nan = nb_nan * 100 / df_taille
    desc_nan = pd.DataFrame([nb_nan, pourcentage_nan],
                            index=['nb_nan', '%_nan'])
    desc_var = pd.concat([desc_type, desc_nan, desc_var])

    return desc_var

# --------------------------------------------------------------------
# -- DESCRIPTION DES VARIABLES QUANTITATIVES
# --------------------------------------------------------------------


def description_variables_quantitatives(dataframe):
    """
    Retourne la description des variables quantitatives du dataframe transmis :
    type, nombre de nan, % de nan et desc
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT : dataframe de description des variables quantitatives
    """
    df_taille = dataframe.shape[0]
    desc_num = dataframe.describe()
    desc_type = pd.DataFrame(desc_num.dtypes, columns=['type']).T
    nb_nan_num = df_taille - desc_num.loc['count'].T
    pourcentage_nan_num = nb_nan_num * 100 / df_taille
    desc_num_nan = pd.DataFrame([nb_nan_num, pourcentage_nan_num],
                                index=['nb_nan', '%_nan'])
    desc_num = pd.concat([desc_type, desc_num_nan, desc_num])

    return desc_num

# --------------------------------------------------------------------
# -- PLAGE DE VALEURS MANQUANTES
# --------------------------------------------------------------------


def distribution_variables_plages_pourc_donnees(
        dataframe, variable, liste_bins):
    """
    Retourne les plages des pourcentages des valeurs pour le découpage transmis
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                variable : variable à découper obligatoire
                liste_bins: liste des découpages facultatif int ou pintervallindex
    @param OUT : dataframe des plages de nan
    """
    nb_lignes = len(dataframe[variable])
    s_gpe_cut = pd.cut(
        dataframe[variable],
        bins=liste_bins).value_counts().sort_index()
    df_cut = pd.DataFrame({'Plage': s_gpe_cut.index,
                           'nb_données': s_gpe_cut.values})
    df_cut['%_données'] = [
        (row * 100) / nb_lignes for row in df_cut['nb_données']]

    return df_cut.style.hide_index()

# --------------------------------------------------------------------
# -- PLAGE DE VALEURS MANQUANTES
# --------------------------------------------------------------------


def distribution_variables_plages_pourc_nan(dataframe, liste_bins=[]):
    """
    Retourne les plages de valeurs manquantes pour le découpage transmis
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                liste_bins: liste des découpages
                            [0, 25, 50, 75, 90, 100] par défaut
    @param OUT : dataframe des plages de nan
    """
    if len(liste_bins) == 0:
        liste_bins = [0, 25, 50, 75, 90]
    liste_bins.append(100)
    # Nombre de variables par plage de pourcentage de valeurs manquantes
    nb_lignes = dataframe.shape[0]
    s_nan = dataframe.isna().sum()
    df_nan = pd.DataFrame({'Variable': s_nan.index,
                           'nb_nan': s_nan.values})
    df_nan['%_nan'] = [(row * 100) / nb_lignes for row in df_nan['nb_nan']]
    df_nan['%_nan_groupe'] = pd.cut(df_nan['%_nan'], bins=liste_bins)
    s_gpe_nan = df_nan['%_nan_groupe'].value_counts().sort_index()
    df_gp_nan = pd.DataFrame({'Plage de %': s_gpe_nan.index,
                              'nb_variable': s_gpe_nan.values})

    return df_gp_nan

# --------------------------------------------------------------------
# -- LISTE DES VARIABLES VIDES D'UN DATAFRAME
# --------------------------------------------------------------------


def affiche_variables_vides(dataframe):
    """
    Affiche le nombre et la liste des colonnes vides d'un dataframe
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT :None
    """
    data_count = dataframe.count()
    s_vide = data_count[data_count == 0]
    print(f'Nombre de variables totalements vides : {len(s_vide)} \n\nListe :')
    print(s_vide.index.tolist())

# --------------------------------------------------------------------
# -- SUPPRESSION DES VARIABLES N'AYANT AUCUNE DONNEE EN LIGNE
# --------------------------------------------------------------------


def suppression_variables_vides(dataframe):
    """
    Suppression des variables vides du dataframe
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT :None
    """
    return dataframe.dropna(axis=1, how='all')


# Liste des colonnes avec '_' ==> à renommer
def formattage_nom_variables(dataframe, car_avant, car_apres):
    """
    Remplacer les caractères avant par les caractères après
    dans le nom des variables du dataframe
    Parameters
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                car_avant : le caractère à remplacer
                car_apres : le caractère de remplacement
    @param OUT : dataframe modifié
    """
    # traces des variables à renommer
    cols_a_renommer = dataframe.columns[dataframe.columns.str.contains(
        car_avant)]
    print(f'{len(cols_a_renommer)} variables renommées \
          \'{car_avant}\' en \'{car_apres}\' : \n\n {cols_a_renommer.tolist()}')

    return dataframe.columns.str.replace(car_avant, car_apres)


# --------------------------------------------------------------------
# -- TRANSFORMATION DES TYPES DE VARIABLE DU DATAFRAME
# --------------------------------------------------------------------
def transfo_type_category(dataframe, colonnes):
    """
    Transforme le type de la liste des colonnes transmises en 'Category'
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                colonnes : liste des variables, obligatoire
    @param OUT :None
    """
    dataframe[colonnes] = dataframe[colonnes].astype('category')


def transfo_type_f64_f32(dataframe):
    """
    Transforme le type des variables de float(64) en float(32)
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT :None
    """
    cols_float64 = dataframe.dtypes[dataframe.dtypes ==
                                    'float64'].index.tolist()
    dataframe[cols_float64] = dataframe[cols_float64].astype('float32')


def transfo_type_object_category(dataframe):
    """
    Transforme les types object du dataframe transmis en category
    si nombre de modalités inférieur à nombre de lignes/2
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT :None
    """
    for col in dataframe.columns.values:
        if dataframe[col].dtype == 'object':
            # print(dataframe[col].unique())
            print('Colonne : ', col)
            if len(dataframe[col].unique()) / len(dataframe[col]) < 0.5:
                dataframe[col] = dataframe[col].astype('category')


# --------------------------------------------------------------------
# -- SUPRESSION VARIABLES POUR UN TAUX DE NAN (%)
# --------------------------------------------------------------------
def suppression_variable_seuil_taux_nan(dataframe, seuil):
    """
    Supprime les variables à partir d'un taux en % de nan.
    Affiche les variables supprimées et les variables conservées
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                seuil : on conserve toutes les variables dont taux de nan <80%
                        entre 0 et 100, integer
    @param OUT : dataframe modifié
    """
    df_appli_nan = round(
        (dataframe.isna().sum() / dataframe.shape[0]) * 100, 2)
    cols = dataframe.columns.tolist()
    # Conservation seulement des variables avec valeurs manquantes >= 80%
    cols_a_garder = df_appli_nan[df_appli_nan.values < seuil].index.tolist()

    cols_info_gen_supprimees = [
        col for col in cols if col not in cols_a_garder]

    dataframe = dataframe[cols_a_garder]

    print(f'Liste des variables éliminées :\n{cols_info_gen_supprimees}\n')

    print(f'Liste des variables conservées :\n{cols_a_garder}')

    return dataframe

# --------------------------------------------------------------------
# -- STATISTIQUES DESCRIPTIVES pour les var quant d'un dataframe
# --------------------------------------------------------------------


def stat_descriptives(dataframe, liste_variables):
    """
    Statistiques descriptives moyenne, mediane, variance, écart-type,
    skewness et kurtosis du dataframe transmis en paramètre
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                liste_variables : colonne dont on veut voir les stat descr
    @param OUT : dataframe des statistiques descriptives
    """
    liste_mean = ['mean']
    liste_median = ['median']
    liste_var = ['var']
    liste_std = ['std']
    liste_skew = ['skew']
    liste_kurtosis = ['kurtosis']
    liste_mode = ['mode']
    liste_cols = ['Desc']
    liste_max = ['Max']
    liste_min = ['Min']

    for col in liste_variables:
        liste_mean.append(dataframe[col].mean())
        liste_median.append(dataframe[col].median())
        liste_var.append(dataframe[col].var(ddof=0))
        liste_std.append(dataframe[col].std(ddof=0))
        liste_skew.append(dataframe[col].skew())
        liste_kurtosis.append(dataframe[col].kurtosis())
        liste_cols.append(col)
        liste_mode.append(dataframe[col].mode().to_string())
        liste_min.append(dataframe[col].min())
        liste_max.append(dataframe[col].max())

    data_stats = [liste_mean, liste_median, liste_var, liste_std, liste_skew,
                  liste_kurtosis, liste_mode, liste_min, liste_max]
    df_stat = pd.DataFrame(data_stats, columns=liste_cols)

    return df_stat.style.hide_index()

# --------------------------------------------------------------------
# -- TRADUCTION DES NOMS DES GROUPES/SOUS-GROUPE EN FRANCAIS
# --------------------------------------------------------------------


def traduire_valeurs_variable(dataframe, colonne_a_traduire, dictionnaire):
    """
    Traduire les valeurs de la colonne du dataframe transmis par la valeur du dictionnaire
    ----------
    @param IN : dataframe : DataFrame, obligatoire
                colonne_a_traduire : colonne dont on veut traduire les valeurs obligatoire
                dictionnaire :dictionnaire clé=à remplacer,
                              valeur = le texte de remplacement oblgatoire
    @param OUT :None
    """
    for cle, valeur in dictionnaire.items():
        dataframe[colonne_a_traduire] = dataframe[colonne_a_traduire].replace(
            cle, valeur)


# -----------------------------------------------------------------------
# -- SPECIFIQUE P3 - CONSERVATION QUE DES PRODUITS FRANCAIS OU OUTRE MEE
# -----------------------------------------------------------------------


def reduction_pays_fr(dataframe):
    """
    Réduction du dataframe aux produits vendus en France et pays d'Outre-Mer
    ----------
    @param IN : dataframe : DataFrame, obligatoire
    @param OUT :None
    """
    return dataframe[(dataframe['countries'].str.contains('de:francia'))
                     | (dataframe['countries'].str.contains('fr:dom-tom'))
                     | (dataframe['countries'].str.contains('fr:f'))
                     | (dataframe['countries'].str.contains('fr:francia'))
                     | (dataframe['countries'].str.contains('fr:francie'))
                     | (dataframe['countries'].str.contains('fr:francija'))
                     | (dataframe['countries'].str.contains('fr:francja'))
                     | (dataframe['countries'].str.contains('fr:frankreich'))
                     | (dataframe['countries'].str.contains('fr:polinesia-francesa'))
                     | (dataframe['countries'].str.contains('Franca'))
                     | (dataframe['countries'].str.contains('France'))
                     | (dataframe['countries'].str.contains('Francia'))
                     | (dataframe['countries'].str.contains('Frankreich'))
                     | (dataframe['countries'].str.contains('Frankrijk'))
                     | (dataframe['countries'].str.contains('French'))
                     | (dataframe['countries'].str.contains('French Guiana'))
                     | (dataframe['countries'].str.contains('French Polynesia'))
                     | (dataframe['countries'].str.contains('Guadeloupe'))
                     | (dataframe['countries'].str.contains('it:frankreich'))
                     | (dataframe['countries'].str.contains('Martinique'))
                     | (dataframe['countries'].str.contains('Mayotte'))
                     | (dataframe['countries'].str.contains('New Caledonia'))
                     | (dataframe['countries'].str.contains('pt:francia'))
                     | (dataframe['countries'].str.contains('Réunion'))
                     | (dataframe['countries'].str.contains('Saint Martin'))
                     | (dataframe['countries'].str.contains('Saint Pierre and Miquelon'))
                     | (dataframe['countries'].str.contains('Sint Maarten'))
                     | (dataframe['countries'].str.contains('Wallis and Futuna'))]

# -----------------------------------------------------------------------
# -- SUPPRESSION DE LA PONCTUATIONN D'UN STR
# -----------------------------------------------------------------------


def suppr_ponct(val):
    """
    Suppression de la ponctuation au texte transmis en paramètres.
    Parameters
    ----------
    val : texte dont on veut supprimer la ponctuation
    Returns
    -------
    Texte sans ponctuation
    """
    if isinstance(val, str):  # éviter les nan
        val = val.lower()
        val = re.compile('[éèêë]+').sub("e", val)
        val = re.compile('[àâä]+').sub("a", val)
        val = re.compile('[ùûü]+').sub("u", val)
        val = re.compile('[îï]+').sub("i", val)
        val = re.compile('[ôö]+').sub("o", val)
        return re.compile('[^A-Za-z" "]+').sub("", val)
    return val

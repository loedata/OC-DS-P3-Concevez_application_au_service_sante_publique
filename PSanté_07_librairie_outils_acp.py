""" Librairie personnelle effectuer des graphiques sur Analyse en
    composantes principales
"""

#! /usr/bin/env python3
# coding: utf-8

# ====================================================================
# Outil visualisation -  projet 3 Openclassrooms
# Version : 0.0.0 - CRE LR 03/03/2021
# ====================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches

# --------------------------------------------------------------------
# -- VERSION
# --------------------------------------------------------------------
__version__ = '0.0.0'

# --------------------------------------------------------------------
# -- AFFICHE LE CERCLE DES CORRELATIONS
# --------------------------------------------------------------------


def display_circles(
        pcs,
        n_comp,
        pca,
        axis_ranks,
        labels=None,
        label_rotation=0,
        lims=None,
        width=16,
        n_cols=3):
    """
    Affiche le cercle des corrélations
    Parameters
    ----------
    pcs :
    n_comp :
    pca :
    axis_ranks :
    labels : , optional
            None par défaut.
    label_rotation :, optional
                    0 par défaut.
    lims : , optional
            None par défaut.
    Returns
    -------
    None.
    """
    n_rows = (n_comp + 1) // n_cols
    fig = plt.figure(figsize=(width, n_rows * width / n_cols))
    # boucle sur les plans factoriels (3 premiers plans -> 6 composantes)
    for i, (d1, d2) in enumerate(axis_ranks):
        if d2 < n_comp:
            ax = fig.add_subplot(n_rows, n_cols, i + 1)
            # limites
            if lims is not None:
                xmin, xmax, ymin, ymax = lims
            elif pcs.shape[1] < 30:
                xmin, xmax, ymin, ymax = -1, 1, -1, 1
            else:
                xmin, xmax, ymin, ymax = min(pcs[d1, :]), max(
                    pcs[d1, :]), min(pcs[d2, :]), max(pcs[d2, :])
            # flèches, si plus de 30, pas de pointes
            if pcs.shape[1] < 30:
                plt.quiver(np.zeros(pcs.shape[1]),
                           np.zeros(pcs.shape[1]),
                           pcs[d1,
                               :],
                           pcs[d2,
                               :],
                           angles='xy',
                           scale_units='xy',
                           scale=1,
                           color='black')
            else:
                lines = [[[0, 0], [x, y]] for x, y in pcs[[d1, d2]].T]
                ax.add_collection(
                    LineCollection(
                        lines,
                        alpha=.1,
                        color='black'))
            # noms de variables
            if labels is not None:
                for text, (x, y) in enumerate(pcs[[d1, d2]].T):
                    if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                        ax.text(
                            x,
                            y,
                            labels[text],
                            fontsize='14',
                            ha='center',
                            va='center',
                            rotation=label_rotation,
                            color="black",
                            alpha=0.5)
            # cercle
            circle = plt.Circle((0, 0), 1, facecolor='none', edgecolor='k')
            ax.add_artist(circle)
            # définition des limites du graphique
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
            # affichage des lignes horizontales et verticales
            ax.plot([-1, 1], [0, 0], color='black', ls='--')
            ax.plot([0, 0], [-1, 1], color='black', ls='--')
            # nom des axes, avec le pourcentage d'inertie expliqué
            ax.set_xlabel(
                'PC{} ({}%)'.format(
                    d1 +
                    1,
                    round(
                        100 *
                        pca.explained_variance_ratio_[d1],
                        1)))
            ax.set_ylabel(
                'PC{} ({}%)'.format(
                    d2 +
                    1,
                    round(
                        100 *
                        pca.explained_variance_ratio_[d2],
                        1)))
            ax.set_title(
                'PCA correlation circle (PC{} and PC{})'.format(
                    d1 + 1, d2 + 1))
    plt.axis('square')
    plt.grid(False)
    plt.tight_layout()
    plt.show()


# --------------------------------------------------------------------
# -- AFFICHE LE PLAN FACTORIEL
# --------------------------------------------------------------------
def display_factorial_planes(
        X_proj,
        n_comp,
        pca,
        axis_ranks,
        couleurs=None,
        labels=None,
        width=16,
        alpha=1,
        n_cols=3,
        illus_var=None,
        lab_on=True,
        size=10):
    """
    Affiche le plan factoriel
    Parameters
    ----------
    X_projected :
    n_comp :
    pca :
    axis_ranks :
    labels : , optional
            None par défaut.
    alpha : , optional
            1 par défaut.
    illustrative_var : , optional
                      None par défaut.
    Returns
    -------
    None.
    """
    n_rows = (n_comp + 1) // n_cols
    fig = plt.figure(figsize=(width, n_rows * width / n_cols))
    # boucle sur chaque plan factoriel
    for i, (d1, d2) in (enumerate(axis_ranks)):
        if d2 < n_comp:
            ax = fig.add_subplot(n_rows, n_cols, i + 1)
            # points
            if illus_var is None:
                ax.scatter(X_proj[:, d1], X_proj[:, d2], alpha=alpha, s=size)
            else:
                illus_var = np.array(illus_var)

                label_patches = []
                colors = couleurs
                i = 0

                for value in np.unique(illus_var):
                    sel = np.where(illus_var == value)
                    ax.scatter(X_proj[sel, d1], X_proj[sel, d2],
                               alpha=alpha, label=value, c=colors[i])
                    label_patch = mpatches.Patch(color=colors[i],
                                                 label=value)
                    label_patches.append(label_patch)
                    i += 1
                    ax.legend(
                        handles=label_patches,
                        bbox_to_anchor=(
                            1.05,
                            1),
                        loc=2,
                        borderaxespad=0.,
                        facecolor='white')
            # labels points
            if labels is not None and lab_on:
                for text_lab, (x, y) in enumerate(X_proj[:, [d1, d2]]):
                    ax.text(x, y, labels[text_lab],
                            fontsize='14', ha='center', va='center')
            # limites
            bound = np.max(np.abs(X_proj[:, [d1, d2]])) * 1.1
            ax.set(xlim=(-bound, bound), ylim=(-bound, bound))
            # lignes horizontales et verticales
            ax.plot([-100, 100], [0, 0], color='grey', ls='--')
            ax.plot([0, 0], [-100, 100], color='grey', ls='--')
            # nom des axes, avec le pourcentage d'inertie expliqué
            ax.set_xlabel(
                'F{} ({}%)'.format(
                    d1 +
                    1,
                    round(
                        100 *
                        pca.explained_variance_ratio_[d1],
                        1)))
            ax.set_ylabel(
                'F{} ({}%)'.format(
                    d2 +
                    1,
                    round(
                        100 *
                        pca.explained_variance_ratio_[d2],
                        1)))
            ax.set_title(
                'Projection des individus (sur F{} et F{})'.format(
                    d1 + 1, d2 + 1))
    plt.grid(False)
    plt.tight_layout()

# --------------------------------------------------------------------
# -- AFFICHE L'EBOULIS DES VALEURS PROPRES
# --------------------------------------------------------------------


def display_scree_plot(pca):
    taux_var_exp = pca.explained_variance_ratio_
    scree = taux_var_exp * 100
    plt.bar(np.arange(len(scree)) + 1, scree, color='SteelBlue')
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax2.plot(np.arange(len(scree)) + 1, scree.cumsum(), c='red', marker='o')
    ax2.set_ylabel('Taux cumulatif de l\'inertie')
    ax1.set_xlabel('Rang de l\'axe d\'inertie')
    ax1.set_ylabel('Pourcentage d\'inertie')
    for i, p in enumerate(ax1.patches):
        ax1.text(
            p.get_width() /
            5 +
            p.get_x(),
            p.get_height() +
            p.get_y() +
            0.3,
            '{:.0f}%'.format(
                taux_var_exp[i] *
                100),
            fontsize=8,
            color='k')
    plt.title('Eboulis des valeurs propres')
    plt.gcf().set_size_inches(8, 4)
    plt.grid(False)
    plt.show(block=False)

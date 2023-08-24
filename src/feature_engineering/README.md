# Recurrent fit

On dispose d'une suite $(t_i, y_i)_{i\in \mathbb{Z}}.$

On veut fitter une fonction linéaire $F(t) = at + b = y$ telle que, pour un $K$ fixé, on atteigne le minimum de

$$l = \sum_{i \leq K} e^{\gamma (t_i - t_{K})} (F(t_i - t_K) - y_i)^2 $$

$$l(a,b) = \sum_{i \leq K} e^{\gamma (t_i - t_{K})} (a (t_i - t_K) + b - y_i)^2 $$

De plus on voudra faire en sorte que les coefficients $a$ et $b$ optimaux soient mis à jour pour chaque $K$ juste grâce au dernier échantillon $(t_K, y_K)$. On calculera les formules qui permettent de mettre à jour ces coefficients de manière récursive.




# Fit pour un $K$ donné

On trouve d'abord la solution pour un $K$ donné.

Pour cela il faut trouver un point tel que $\frac{\partial}{\partial a} l(a,b) = \frac{\partial}{\partial b} l (a,b) = 0$.

Annulons la dérivée par rapport à $b$ :

$$\frac{\partial l}{\partial b} (a,b) = 2 \sum_{i \leq K} e^{\gamma (t_i - t_{K})} (a (t_i - t_K) + b - y_i) = 0$$

vrai si

$$b \sum_{i \leq K} e^{\gamma (t_i - t_{K})}   =\sum_{i \leq K} e^{\gamma (t_i - t_{K})} (y_i - a (t_i - t_K))$$

C'est à dire si

$$b = \hat{b}(a) = \frac{\sum_{i \leq K} e^{\gamma (t_i - t_{K})} (y_i - a (t_i - t_K) )}{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}}$$

En réinjectant dans l'expression de $l(a,b)$ on obtient

$$l(a,\hat{b}(a)) = \sum_{i \leq K} e^{\gamma (t_i - t_{K})} (a (t_i - t_K) + \hat{b}(a) - y_i)^2 $$

En dérivant l'expression ci-dessus par rapport à $a$ et en égalant à zéro

$$\sum_{i \leq K} 2 e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K + \frac{\partial \hat{b}}{\partial a}\Big)(a (t_i - t_K) + \hat{b}(a) - y_i)  = 0$$

On obtient

$$\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K + \frac{\partial \hat{b}}{\partial a}\Big) \Bigg(a (t_i - t_K) + \frac{\sum_{j \leq K} e^{\gamma (t_j - t_{K})} (y_j - a (t_j - t_K) )}{\sum_{j \leq K} e^{\gamma (t_j - t_{K})}} - y_i\Bigg)  = 0$$

Avec 

$$\frac{\partial \hat{b}}{\partial a} = - \frac{\sum_{i \leq K} e^{\gamma (t_i - t_{K})} (t_i - t_K) }{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}} = - \bar{T}_{K}$$

Il faut donc

$$a \sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K + \frac{\partial \hat{b}}{\partial a}\Big) \Bigg(t_i - t_K - \frac{\sum_{j \leq K} e^{\gamma (t_j - t_{K})}   (t_j - t_K) }{\sum_{j \leq K} e^{\gamma (t_j - t_{K})}} \Bigg)$$ 
$$ = \sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K + \frac{\partial \hat{b}}{\partial a}\Big) \Bigg( y_i - \frac{\sum_{j \leq K} e^{\gamma (t_j - t_{K})} y_j }{\sum_{j \leq K} e^{\gamma (t_j - t_{K})}} \Bigg)$$

C'est à dire

$$ a \sum_{i \leq K} e^{\gamma (t_i  - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big)^2  = \sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big) \Big( y_i - \bar{Y}_{K} \Big)$$

avec

$$\bar{Y}_{K}  = \frac{\sum_{j \leq K} e^{\gamma (t_j - t_{K})} y_j }{\sum_{j \leq K} e^{\gamma (t_j - t_{K})}}$$


Enfin :

$$ a = \hat{a} = \frac{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big) \Big( y_i - \bar{Y}_{K} \Big)}{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big)^2 }$$

En réinjectant et en simplifiant l'expression :

$$\hat{b}(\hat{a}) = \bar{Y}_{K} - \hat{a} \bar{T}_{K}$$

# Calcul de $\hat{a}$ récursif

Pour le dénominateur, remarquons que

$$\sum_{j \leq K} e^{\gamma (t_j - t_{K})}  \Big(t_j - t_K - \bar{T}_{K}\Big)^2 = \sum_{j \leq K} e^{\gamma (t_j - t_{K})}  \Big((t_j - t_K)^2 - 2\bar{T}_{K} (t_j - t_K) + \bar{T}_{K}^2 \Big)
$$

$$=\sum_{j \leq K} e^{\gamma (t_j - t_{K})}  \Big((t_j - t_K)^2 - \bar{T}_{K}^2 \Big)$$

Car

$$\sum_{j \leq K} e^{\gamma (t_j - t_{K})}  \bar{T}_{K} (t_j - t_K)  = \bar{T}_{K}^2 \sum_{j \leq K} e^{\gamma (t_j - t_{K})}  $$

Pour le numérateur on a

$$\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big) \Big( y_i - \bar{Y}_{K} \Big)$$

Celui ci se sépare en quatre termes

$$\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big((t_i - t_K) y_i - \bar{T}_{K} y_i -  (t_i - t_K) \bar{Y}_{K} + \bar{Y}_{K} \bar{T}_{K} \Big)$$

# Formules récursives

## Weights

$$W(K + 1) = \sum_{i \leq K + 1} e^{\gamma (t_i - t_{K + 1})} = e^{\gamma(t_{K} - t_{K + 1})}\sum_{i \leq K + 1} e^{\gamma (t_i - t_{K}) }$$
$$= 1 + e^{\gamma(t_{K} - t_{K + 1})} \sum_{i \leq K } e^{\gamma (t_i - t_{K}) } $$
$$= 1 + e^{\gamma(t_{K} - t_{K + 1})}  W(K)$$

## Time differences
$$T(K + 1) = \sum_{i \leq K + 1} e^{\gamma (t_i - t_{K + 1})} (t_i - t_{K+1})$$

$$=\sum_{i \leq K} e^{\gamma (t_i - t_{K + 1})} (t_i - t_K) + \sum_{i \leq K} e^{\gamma (t_i - t_{K + 1})} (t_K - t_{K+1})$$

$$= e^{\gamma (t_{K} - t_{K+1})} \sum_{i \leq K} e^{\gamma (t_i - t_{K})} (t_i - t_K) + e^{\gamma (t_i - t_{K})} \sum_{i \leq K} e^{\gamma (t_i - t_{K})} (t_K - t_{K+1})$$

$$e^{\gamma (t_{K} - t_{K+1})} \Big(T(K) + W(K) (t_K - t_{K+1})\Big)$$

## Values

$$Y(K+1) = \sum_{j \leq K+1} e^{\gamma (t_j - t_{K+1})} y_j$$
$$= y_{K+1} + \sum_{j \leq K} e^{\gamma (t_j - t_{K+1})} y_j$$

$$= y_{K+1} + e^{\gamma (t_{K} - t_{K+1})} \sum_{j \leq K} e^{\gamma (t_j - t_{K})} y_j$$

$$= y_{K+1} + e^{\gamma (t_{K} - t_{K+1})} Y(K)$$

## Squared time differences

$$S(K+1) = \sum_{j \leq K+1} e^{\gamma (t_j - t_{K+1})}  (t_j - t_{K+1})^2$$

$$= e^{\gamma (t_{K} - t_{K+1})} \sum_{j \leq K} e^{\gamma (t_j - t_{K})}  (t_j - t_{K+1})^2$$

$$= e^{\gamma (t_{K} - t_{K+1})} \sum_{j \leq K} e^{\gamma (t_j - t_{K})}  (t_j - t_{K} + t_K - t_{K+1})^2$$

$$= e^{\gamma (t_{K} - t_{K+1})} \sum_{j \leq K} e^{\gamma (t_j - t_{K})}  \Bigg((t_j - t_{K})^2 + 2(t_j - t_K)(t_{K} - t_{K+1}) + (t_K - t_{K+1})^2 \Bigg)$$

$$= e^{\gamma (t_{K} - t_{K+1})} \Bigg( S(K) + 2T(K)(t_{K} - t_{K+1}) + W(K)(t_K - t_{K+1})^2 \Bigg)$$

## Time value product

$$P(K+1) = \sum_{i \leq K+1} e^{\gamma (t_i - t_{K+1})}  (t_i - t_{K+1}) y_i$$

$$= e^{\gamma (t_K - t_{K+1})} \sum_{i \leq K} e^{\gamma (t_i - t_{K})}  (t_i - t_{K+1}) y_i$$

$$= e^{\gamma (t_K - t_{K+1})} \sum_{i \leq K} e^{\gamma (t_i - t_{K})}  (t_i - t_{K} + t_K - t_{K+1}) y_i$$



$$= e^{\gamma (t_K - t_{K+1})} \Big(P(K) + (t_K - t_{K+1})Y(K)\Big)$$

## Expressions récursives des quantités d'intérêt
Finalement on obtient : 
#
$$\bar{Y}_{K}  = \frac{Y(K)}{W(K)}$$

#
$$\bar{T}_{K} =\frac{\sum_{i \leq K} e^{\gamma (t_i - t_{K})} (t_i - t_K) }{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}} = \frac{T(K)}{W(K)}$$

#
$$\hat{a} = \frac{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big) \Big( y_i - \bar{Y}_{K} \Big)}{\sum_{i \leq K} e^{\gamma (t_i - t_{K})}  \Big(t_i - t_K - \bar{T}_{K}\Big)^2 }$$

Dont le dénominateur vaut

$$S(K) - W(K)\bar{T}_K^2$$

Et dont le numérateur vaut

$$P(K) - Y(K)\bar{T}_K - \bar{Y}_K T(K)+ \bar{T}_K \bar{Y}_K W(K)$$
$$= P(K) - \bar{T}_K \bar{Y}_K W(K)$$

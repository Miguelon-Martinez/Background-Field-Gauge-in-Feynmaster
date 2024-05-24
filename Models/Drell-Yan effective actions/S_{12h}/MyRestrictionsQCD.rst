M$Restrictions = {

   (* Some restrictions for matricial structures: *)
   TensDot[HC[X_], HC[Y_], HC[Z_]][i_, j_] :> Conjugate[X[k,i]] Conjugate[Y[l,k]] Conjugate[Z[j,l]],
   TensDot[HC[X_], HC[Y_], Z_][i_, j_] :> Conjugate[X[k,i]] Conjugate[Y[l,k]] Z[l,j],
   TensDot[HC[X_], Y_, HC[Z_]][i_, j_] :> Conjugate[X[k,i]] Y[k,l] Conjugate[Z[j,l]],
   TensDot[HC[X_], Y_, Z_][i_, j_] :> Conjugate[X[k,i]] Y[k,l] Z[l,j],
   TensDot[X_, HC[Y_], HC[Z_]][i_, j_] :> X[i,k] Conjugate[Y[l,k]] Conjugate[Z[j,l]],
   TensDot[X_, HC[Y_], Z_][i_, j_] :> X[i,k] Conjugate[Y[l,k]] Z[l,j],
   TensDot[X_, Y_, HC[Z_]][i_, j_] :> X[i,k] Y[k,l] Conjugate[Z[j,l]],
   TensDot[X_, Y_, Z_][i_, j_] :> X[i,k] Y[k,l] Z[l,j],
   TensDot[HC[X_], HC[Y_]][i_, j_] :> Conjugate[X[k,i]] Conjugate[Y[j,k]],
   TensDot[HC[X_], Y_][i_, j_] :> Conjugate[X[k,i]] Y[k,j],
   TensDot[X_, HC[Y_]][i_, j_] :> X[i,k] Conjugate[Y[j,k]],
   TensDot[X_, Y_][i_, j_] :> X[i,k] Y[k,j],

   (* Remaining restrictions: *)
   Muq[i_, j_] :> 0 /; NumericQ[i] && NumericQ[j] && (i!= j),
   Muq[i_, j_] :> muq[i] /; NumericQ[i] && NumericQ[j] && (i == j),
   muq[1] :> mu, muq[2] :> mc, muq[3] :> mt,

   dZuq[i_, j_] :> 0 /; NumericQ[i] && NumericQ[j] && (i!= j),

   dMuq[i_, j_] :> 0 /; NumericQ[i] && NumericQ[j] && (i!= j),
   dMuq[i_, j_] :> dmuq[i] /; NumericQ[i] && NumericQ[j] && (i == j),   
   dmuq[1] :> dmu, dmuq[2] :> dmc, dmuq[3] :> dmt   
}

\
# WilsonTheta 

```cpp
#include <analysis/integrator/WilsonTheta.h>
```

class WilsonTheta: public TransientIntegrator\

MovableObject\
Integrator\
IncrementalIntegrator\
TransientIntegrator\

\
WilsonTheta is a subclass of TransientIntegrator which implements the
Wilson$\Theta$ method. In the Wilson$\Theta$ method, to determine the
velocities, accelerations and displacements at time $t + \theta \Delta
t$, $\theta \ge 1.37$, for $\U_{t+ \theta \Delta t}$

$$\R (\U_{t + \theta \Delta t}) = \P(t + \theta \Delta t) -
\F_I(\Udd_{t+ \theta \Delta t}) 
- \F_R(\Ud_{t + \theta \Delta t},\U_{t + \theta \Delta t})$$

where we use following functions to relate $\Ud_{t + \theta
\Delta t}$ and $\Udd_{t + \theta \Delta t}$ to $\U_{t + \theta \Delta
t}$ and the response quantities at time $t$:

$$\dot \U_{t + \theta \Delta t} = \frac{3}{\theta \Delta t} \left(
\U_{t + \theta \Delta t} - \U_t \right)
 - 2 \dot \U_t + \frac{\theta \Delta t}{2} \ddot \U_t$$

$$\ddot \U_{t + \theta \Delta t} = \frac{6}{\theta^2 \Delta t^2}
\left( \U_{t+\theta \Delta t} - \U_t \right)
 - \frac{6}{\theta \Delta t} \dot \U_t -2 \Udd_t$$

which results in the following for determining the responses at
$t + \theta \Delta t$

$$\left[ \frac{6}{\theta^2 \Delta t^2} \M + \frac{3}{\theta \Delta t}
\C + \K \right] \Delta \U_{t + \theta \Delta t}^{(i)} = \P(t + \theta
\Delta t) - \F_I\left(\Udd_{t+\theta \Delta  t}^{(i-1)}\right) 
- \F_R\left(\Ud_{t + \theta \Delta t}^{(i-1)},\U_{t + \theta \Delta
t}^{(i-1)}\right)$$

The response quantities at time $t + \Delta t$ are then determined using
the following

$$\Udd_{t + \Delta t} = \Udd_t + \frac{1}{\theta} \left( \Udd_{t +
\theta \Delta t} - \Udd_t \right)$$

$$\Ud_{t + \Delta t} = \Ud_t + \frac{\Delta t}{2}\left( \Udd_{t +
\Delta t} + \Udd_t \right)$$

$$\U_{t + \Delta t} = \U_t + \Delta t\Ud_t + \frac{\Delta t^2}{6}\left(
\Udd_{t + \Delta t} + 2 \Udd_t \right)$$\

// Constructors\

\

\
// Destructor\

\
// Public Methods\

\

\

\

// Public Methods for Output\

\

\

The integer `INTEGRATOR_TAGS_WilsonTheta` is passed to the
TransientIntegrator constructor. $\Theta$ is set to 0.0. This
constructor should only be invoked by an FEM_ObjectBroker.

Sets $\Theta$ to *theta*, $\gamma$ to $(1.5 - \alpha)$ and $\beta$ to
$0.25*\alpha^2$. addition, a flag is set indicating that Rayleigh
damping will not be used.

Sets $\Theta$ to *theta*, $\gamma$ to $(1.5 - \alpha)$ and $\beta$ to
$0.25*\alpha^2$. In addition, a flag is set indicating that Rayleigh
damping will not be used.

This constructor is invoked if Rayleigh damping is to be used, i.e.
$\D = \alpha_M M + \beta_K K$. Sets $\Theta$ to *theta*, $\gamma$ to
$(1.5 - \alpha)$, $\beta$ to $0.25*\alpha^2$, $\alpha_M$ to *alphaM* and
$\beta_K$ to *betaK*. Sets a flag indicating whether the incremental
solution is done in terms of displacement or acceleration to *dispFlag*
and a flag indicating that Rayleigh damping will be used.

\
Invokes the destructor on the Vector objects created.

\
This tangent for each FE_Element is defined to be $\K_e = c1 \K
+ c2  \D + c3 \M$, where c1,c2 and c3 were determined in the last
invocation of the `newStep()` method. Returns $0$ after performing the
following operations:

::: {.tabbing}
while ̄ while w̄hile ̄ if (RayleighDamping == false) {\
theEle-$>$zeroTang()\
theEle-$>$addKtoTang(c1)\
theEle-$>$addCtoTang(c2)\
theEle-$>$addMtoTang(c3)\
} else {\
theEle-$>$zeroTang()\
theEle-$>$addKtoTang(c1 + c2 \* $\beta_K$)\
theEle-$>$addMtoTang(c3 + c2 \* $\alpha_M$)\
}
:::


```{.cpp}
int formNodTangent(DOF_Group \*theDof);
```

This performs the following:

::: {.tabbing}
while ̄ while w̄hile ̄ theDof-$>$zeroUnbalance()\
if (RayleighDamping == false)\
theDof-$>$addMtoTang(c3)\
else\
theDof-$>$addMtoTang(c3 + c2 \* $\alpha_M$)\
:::


```{.cpp}
int domainChanged(void);
```

If the size of the LinearSOE has changed, the object deletes any old
Vectors created and then creates $6$ new Vector objects of size equal to
*theLinearSOE-$>$getNumEqn()*. There is a Vector object created to store
the current displacement, velocity and accelerations at times $t$ and
$t + \Delta t$ (between `newStep()` and `commit()` the $t +
\Delta t$ quantities store $t + \Theta \Delta t$ quantities). The
response quantities at time $t + \Delta t$ are then set by iterating
over the DOF_Group objects in the model and obtaining their committed
values. Returns $0$ if successful, otherwise a warning message and a
negative number is returned: $-1$ if no memory was available for
constructing the Vectors.

```{.cpp}
int newStep(double $\Delta t$);
```

The following are performed when this method is invoked:

1.  First sets the values of the three constants *c1*, *c2* and *c3*:
    *c1* is set to $1.0$, *c2* to $3 / (\Theta
    \Delta t)$ and *c3* to $6 / (\Theta \Delta t)^2)$.

2.  Then the Vectors for response quantities at time $t$ are set equal
    to those at time $t + \Delta t$.

    ::: {.tabbing}
    while w̄hile w̄hile w̄hile ̄ $\U_t = \U_{t + \Delta t}$\
    $\Ud_t = \Ud_{t + \Delta t}$\
    $\Udd_t = \Udd_{t + \Delta t}$
    :::

3.  Then the velocity and accelerations approximations at time
    $t + \Theta \Delta t$ are set using the difference approximations,

    ::: {.tabbing}
    while w̄hile w̄hile w̄hile ̄ $\U_{t + \theta \Delta t} = \U_t$\
    $\dot \U_{t + \theta \Delta t} = - 2 \dot \U_t + \frac{\theta
    \Delta t}{2} \ddot \U_t$\
    $\ddot \U_{t + \theta \Delta t} = - \frac{6}{\theta \Delta t}
    \dot \U_t -2 \Udd_t$
    :::

4.  The response quantities at the DOF_Group objects are updated with
    the new approximations by invoking `setResponse()` on the
    AnalysisModel with quantities at time $t + \Theta \Delta t$.

    ::: {.tabbing}
    while w̄hile w̄hile w̄hile ̄
    theModel-$>$setResponse$(\U_{t + \theta \Delta t}, \Ud_{t+\theta
    \Delta t}, \Udd_{t+ \theta \Delta t})$
    :::

5.  current time is obtained from the AnalysisModel, incremented by
    $\Theta \Delta t$, and `applyLoad(time, 1.0)`{.cpp} is invoked on the
    AnalysisModel.

6.  Finally `updateDomain()` is invoked on the AnalysisModel.

The method returns $0$ if successful, otherwise a negative number is
returned: $-1$ if $\gamma$ or $\beta$ are $0$, $-2$ if *dispFlag* was
true and $\Delta t$ is $0$, and $-3$ if `domainChanged()` failed or has
not been called.

```{.cpp}
int update(const Vector &$\Delta U$);
```

Invoked this first causes the object to increment the DOF_Group response
quantities at time $t + \Theta \Delta t$. The displacement Vector is
incremented by $c1 * \Delta U$, the velocity Vector by $c2 * \Delta U$,
and the acceleration Vector by $c3 * \Delta U$. The response quantities
at the DOF_Group objects are then updated with the new approximations by
invoking `setResponse()` on the AnalysisModel with displacements,
velocities and accelerations at time $t + \Theta \Delta t$. Finally
`updateDomain()` is invoked on the AnalysisModel.

::: {.tabbing}
while w̄hile w̄hile w̄hile ̄ $\U_{t + \theta \Delta t} += \Delta \U$\
$\dot \U_{t + \theta \Delta t} += \frac{3}{\theta \Delta t}
\Delta \U$\
$\ddot \U_{t + \theta \Delta t} += \frac{6}{\theta^2 \Delta
t^2} \Delta \U$\
theModel-$>$setResponse$(\U_{t + \alpha \theta t}, \Ud_{t+\theta
\Delta t}, \Udd_{t+ \theta \Delta t})$\
theModel-$>$updateDomain()
:::

Returns $0$ if successful. A warning message is printed and a negative
number returned if an error occurs: $-1$ if no associated AnalysisModel,
$-2$ if the Vector objects have not been created, $-3$ if the Vector
objects and $\Delta U$ are of different sizes.

```{.cpp}
int commit(void);
```

First the quantities at time $t + \Delta t$ are determined using the
quantities at time $t$ and $t + \Theta \Delta t$. Then the response
quantities at the DOF_Group objects are updated with the new
approximations by invoking `setResponse()` on the AnalysisModel with
displacement, velocity and accelerations at time $t +
\Delta t$. The time is obtained from the AnalysisModel and $(\Theta
-1) \Delta t$ is subtracted from the value. The time is set in the
Domain by invoking `setCurrentDomainTime(time)` on the AnalysisModel.
Finally `updateDomain()` and `commitDomain()` are invoked on the
AnalysisModel.

::: {.tabbing}
while w̄hile w̄hile w̄hile ̄
$\Udd_{t + \Delta t} = \Udd_t + \frac{1}{\theta} \left( \Udd_{t +
\theta \Delta t} - \Udd_t \right)$\
$\Ud_{t + \Delta t} = \Ud_t + \frac{\Delta t}{2}\left( \Udd_{t +
\Delta t} + \Udd_t \right)$\
$\U_{t + \Delta t} = \U_t + \Delta t\Ud_t + \frac{\Delta t^2}{6}\left(
\Udd_{t + \Delta t} + 2 \Udd_t \right)$\
theModel-$>$setResponse$(\U_{t + \Delta t}, \Ud_{t+
\Delta t}, \Udd_{t+\Delta t})$\
time = theModel-$>$getDomainTime()\
time -= $(\theta -1) * \Delta t$\
theModel-$>$setTime(time)\
theModel-$>$commitDomain()
:::

Returns $0$ if successful, a warning message and a negative number if
not: $-1$ if no AnalysisModel associated with the object and $-2$ if
`commitDomain()` failed.
*int sendSelf(int commitTag, Channel &theChannel);* \
Places $\Theta$, rayleigh damping flag, $\alpha_M$ and $\beta_K$ in a
vector if size 4 and invokes *sendVector* on the Channel with this
Vector. Returns $0$ if successful, a warning message is printed and a
$-1$ is returned if *theChannel* fails to send the Vector.
*int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker
&theBroker);* \
Receives in a Vector of size 4 the value of $\Theta$, the rayleigh
damping flag, $\alpha_M$ and $\beta_K$.. Returns $0$ if successful, a
warning message is printed, $\Theta$ is set to $0$, the rayleigh damping
flag to *false*, and a $-1$ is returned if *theChannel* fails to receive
the Vector.

```{.cpp}
int Print(OPS_Stream &s, int flag = 0);
```

The object sends to $s$ its type, the current time, $\alpha$, $\gamma$
and $\beta$.

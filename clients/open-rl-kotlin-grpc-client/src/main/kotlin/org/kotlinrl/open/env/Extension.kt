package org.kotlinrl.open.env

import open.rl.env.EnvOuterClass.Info
import open.rl.env.EnvOuterClass.Observation
import open.rl.env.EnvOuterClass.StepResponse

operator fun StepResponse.component1(): Observation = observation
operator fun StepResponse.component2() = reward
operator fun StepResponse.component3() = terminated
operator fun StepResponse.component4() = truncated
operator fun StepResponse.component5(): Info = info

import z from "zod"

export const ProgressionSchema = z.object({  	
  challenge_id: z.number(),
  current_progress: z.number(),
  completed: z.number()
})

export type Progression = z.infer<typeof ProgressionSchema>

export const UpdateProgressionSchema = z.object({  	
  challenge_id: z.number(),
  score: z.number()
})

export type UpdateProgression = z.infer<typeof UpdateProgressionSchema>

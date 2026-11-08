# EXP-058 Result: Held-Out Thresholded Semantic Entity Resolution

Aggregate:

    Threshold=0.39
    OverallAccuracy=0.7500
    ResolvableEntityAccuracy=0.5000
    AbstentionAccuracy=1.0000
    FalsePositiveResolutionRate=0.0000

The fixed threshold preserved perfect abstention, but two positive cases confidently linked to the wrong neighboring entity.

Failures:

    "group that runs the Atlas authentication service"
    predicted: atlas (service)
    gold: platform_reliability (team)

    "team that maintains the production session-metadata cache"
    predicted: solstice (service)
    gold: identity_foundations (team)

Both errors cross entity types. This suggests the next diagnostic should constrain candidate ranking by the intended entity type while keeping the threshold, embeddings, profiles, and mention spans fixed.

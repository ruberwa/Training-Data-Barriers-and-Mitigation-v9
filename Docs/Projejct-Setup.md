**Title:** Set up the analysis of training-data barriers and mitigation strategies

## Project status
- Studies training-data barriers and mitigation strategies in weed detection, segmentation, and classification
- Source dataset and country map are in place
- Analysis steps are not implemented yet
- No tables or figures have been produced

## Analysis-ready tables
- **Study master:** one row per study, with task, environment, year, and dataset size
- **Barrier-mitigation map:** which barrier is linked to which mitigation inside each study
- **Performance results:** baseline versus mitigation only when the study, instance, metric, and metric family match exactly
- **Performance linkage audit:** every mitigation result, including rows with no exact baseline
- **Evidence quality:** risk-of-bias and credibility judgments for each study
- **Sources:** source and justification records for each study

## Statistical tables
- **Publication year:** how many studies were published in each year
- **Task distribution:** how many studies cover detection, segmentation, and classification
- **Environment distribution:** how many studies are field, UAV, greenhouse, lab, or controlled
- **Geographic distribution:** how many studies come from each country
- **Dataset size summary:** image-count spread within each task
- **Barrier category prevalence:** how often each barrier category is reported
- **Normalized barrier prevalence:** how often each specific barrier is reported
- **Barrier by task:** which barriers appear in each task
- **Barrier co-occurrence:** which barriers are reported together
- **Mitigation category prevalence:** how often each mitigation category is used
- **Mitigation strategy prevalence:** how often each specific strategy is used
- **Mitigation by task:** which strategies appear in each task
- **Synthetic method profile:** how often data augmentation and synthetic data generation are used
- **Synthetic barrier profile:** which barriers those synthetic methods are paired with
- **Metric coverage:** which performance metrics are reported for each task
- **Evidence quality profile:** how studies are judged on each quality criterion
- **Task-barrier test:** whether barrier profiles differ across the three tasks
- **Task-barrier counts:** study counts behind that test
- **Barrier-mitigation test:** whether particular mitigations are associated with particular barriers
- **Barrier-mitigation counts:** how often each barrier is paired with each mitigation
- **Barrier-mitigation row percent:** those pairings as a share of each barrier
- **Study-level effects:** one performance gain per study and task
- **Task synthesis:** median gain and interval for each task
- **Continuous moderators:** whether baseline performance and dataset size explain differences in gain
- **Environment subgroups:** gain compared across environments
- **Mitigation subgroups:** gain compared across mitigation strategies
- **Barrier type moderator:** gain compared across barrier types
- **Barrier-performance linkage audit:** which performance rows are tied to a barrier and mitigation
- **Auditable quality criteria:** counts for each credibility judgment
- **Sensitivity synthesis:** whether the gain result holds under stricter quality rules
- **Leave-one-study-out:** whether one study changes the task median
- **Method study effects:** study-level gain for synthetic methods and other methods
- **Method raw summary:** unadjusted comparison of those methods
- **Baseline-adjusted method contrasts:** whether synthetic methods still differ after accounting for baseline performance
- **Synthetic subtypes by task:** data augmentation versus synthetic data generation within each task

## Test plan
- [ ] Source workbook and country map are available
- [ ] No generated tables, logs, or figures are included

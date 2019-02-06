## Python script to modify \<version> of pom.xml

### Problem Description

Please use the provided pom.xml and create a python script which customizes the project pom version 
to match this pattern `<version>ci_{git hub org name here}_{branch name here}-SNAPSHOT</version>`.
As an example, when this script runs on code that lives in the `Team_Foo` git hub organization on 
a branch named `Bar`, the resulting version would be `ci_Team_Foo_Bar-SNAPSHOT`.
 
##### Python script requirements
 * It must validate the pom is syntactically correct
 * It must confirm the existing version is a snapshot prior to making any changes
 * The resulting pom version needs to match this format `ci_{git hub org name here}_{branch name here}-SNAPSHOT`
 * Unit tests are an added bonus
 * Execution within a docker container is an extra bonus
 
Please provide details on how to execute your solution, as well as any presumptions/issues/etc that you 
feel is appropriate for the reviewer to be aware of.

#### Steps
1. export GIT_REPO_DIR=\<path-to-mvnproject-git-repo>
2. docker-compose up
3. check logs in ./logs

#### Assumptions
1. pom.xml resides in $GIT_REPO_DIR and not in any sub-dirs
2. user has docker and docker-compose configured

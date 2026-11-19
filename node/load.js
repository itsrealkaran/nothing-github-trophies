"use strict";

const { fail, graphql, ownedRepos } = require("./github");

const LADDER = ["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"];
const STEPS = {
  Stars: [2000, 700, 200, 100, 50, 30, 10, 1],
  Contributions: [4000, 2000, 1000, 500, 200, 100, 10, 1],
  Followers: [1000, 400, 200, 100, 50, 20, 10, 1],
  Issues: [1000, 500, 200, 100, 50, 20, 10, 1],
  Pulls: [1000, 500, 200, 100, 50, 20, 10, 1],
  Repos: [50, 45, 40, 35, 30, 20, 10, 1],
};

function rank(score, steps) {
  for (let index = 0; index < LADDER.length; index += 1) {
    if (score >= steps[index]) return LADDER[index];
  }
  return "—";
}

async function load(login) {
  const query = `
    query($login: String!) {
      user(login: $login) {
        followers { totalCount }
        issues { totalCount }
        pullRequests { totalCount }
        repositories(first: 1, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
          totalCount
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }
    `;
  const data = await graphql(query, { login });
  const user = data && data.user;
  if (!user) fail("no github user named " + login);
  const owned = await ownedRepos(login);
  const stars = owned.repos.reduce((sum, repo) => sum + (repo.stargazers_count || 0), 0);
  const year = user.contributionsCollection;
  const contributions = year.totalCommitContributions + (year.restrictedContributionsCount || 0);
  const scores = [
    ["Stars", stars],
    ["Contributions", contributions],
    ["Followers", user.followers.totalCount],
    ["Issues", user.issues.totalCount],
    ["Pulls", user.pullRequests.totalCount],
    ["Repos", user.repositories.totalCount],
  ];
  return {
    login,
    rows: scores.map(([title, score]) => ({ title, score, rank: rank(score, STEPS[title]) })),
    private_stars: owned.own,
  };
}

module.exports = { load };

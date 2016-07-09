import numpy
import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import display
from matplotlib.patches import Circle, Rectangle, Arc

print('hello world')

# Lebron Jame's shot chart for 2015-16 season.
shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?DateFrom=&DateTo=&GameID=&ContextMeasure=FGA&Position=&RookieYear=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=PerGame&Period=0&PlayerID=2544&Season=2015-16&SeasonSegment=&SeasonType=Playoffs&TeamID=0&VsConference=&VsDivision='

# Get the page with all the data
response = requests.get(shot_chart_url)
# Grab the headers to be used as headers in our DataFrame
# ResultSets is in the JSON output from the shot_chart_url
headers = response.json()['resultSets'][0]['headers']
# Grab the shot chart Data
shots = response.json()['resultSets'][0]['rowSet']
# Create a Pandas dframe using the scraped shot chart Data
shot_df = pd.DataFrame(shots, columns=headers)

# Show data frame head for context.
# with pd.option_context('display.max_columns', None):
#     display(shot_df.head())


# Plot the data.
# sns.set_style("white")
# sns.set_color_codes()
# plt.figure(figsize=(12, 11))
# plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
# plt.show()

# The plot above is the inverese of what it should be.
# To show this we can plot all the shots categoriezed as "RIGHT SIDE(R)"
# The plot shows these to the viewers right, but are actually taken
# from the left side of the hoop!


# Drawing the court.
def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes isn't provided to plot, just get the current one
    if ax is None:
        ax = plt.gca()

    # Create hoop
    # Diameter is 18" or radius of 9" which is a value of 7.5 in our
    # coordinate system according to shots plotted and distances given.

    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The Pain
    # Outer box of paint, width = 6ft, height = 19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Top free-throw arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Bottom free-throw arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, linestyle='dashed')

    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

# # Draw the court and flip it around. Also adjust to only be half court.
# plt.figure(figsize=(12,11))
# plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
# draw_court()
# # Adjust plot limits to just fit in half court
# plt.xlim(-250,250)
# # Descending values along th y axis from bottom to top
# # in order to place the hoop by the top of plot
# plt.ylim(422.5, -47.5)
# # get rid of axis tick labels
# # plt.tick_params(labelbottom=False, labelleft=False)
# plt.show()

joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None,
                                 kind='scatter',space=0,alpha=0.5)
joint_shot_chart.fig.set_size_inches(12,11)

# Joint plot has 3 Axes, firt one called ax_joint is where we draw court
ax = joint_shot_chart.ax_joint
draw_court(ax)

# Adjust limits of axis and orentation to be half court
ax.set_xlim(-250,250)
ax.set_ylim(422.5,-47.5)

# Get rid of lables and tick marks
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(labelbottom='off',labelleft='off')

# Add title
ax.text(-60,-160,'LeBron James FGA 2015-2016 Reg. Season', verticalalignment='top')

# Add datasource and author
ax.text(-250,460,'Data Source: stats.nba.com' '\nAuthor: Chris Meringolo',
        fontsize=12)
plt.show()

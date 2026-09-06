import os
import zipfile
import xml.etree.ElementTree as ET

def create_tableau_xml():
    twb_xml = """<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2020.4.0' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='24' />
  </preferences>

  <datasources>
    <!-- Primary Datasource: dim_titles -->
    <datasource caption='dim_titles' inline='true' name='federated.dim_titles' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='dim_titles' name='textscan.dim_titles'>
            <connection class='textscan' directory='.' filename='dim_titles.csv' password='' server='' />
          </named-connection>
        </named-connections>

        <relation connection='textscan.dim_titles' name='dim_titles.csv' table='[dim_titles#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='string' name='show_id' ordinal='0' />
            <column datatype='string' name='type' ordinal='1' />
            <column datatype='string' name='title' ordinal='2' />
            <column datatype='string' name='director' ordinal='3' />
            <column datatype='string' name='cast' ordinal='4' />
            <column datatype='string' name='country' ordinal='5' />
            <column datatype='date' name='date_added' ordinal='6' />
            <column datatype='integer' name='release_year' ordinal='7' />
            <column datatype='string' name='rating' ordinal='8' />
            <column datatype='string' name='duration' ordinal='9' />
            <column datatype='string' name='listed_in' ordinal='10' />
            <column datatype='string' name='description' ordinal='11' />
            <column datatype='integer' name='year_added' ordinal='12' />
            <column datatype='integer' name='month_added' ordinal='13' />
            <column datatype='string' name='month_name_added' ordinal='14' />
            <column datatype='integer' name='quarter_added' ordinal='15' />
            <column datatype='string' name='day_name_added' ordinal='16' />
            <column datatype='real' name='duration_minutes' ordinal='17' />
            <column datatype='integer' name='duration_seasons' ordinal='18' />
            <column datatype='real' name='content_age_at_add' ordinal='19' />
            <column datatype='integer' name='is_fresh_add' ordinal='20' />
            <column datatype='string' name='primary_country' ordinal='21' />
            <column datatype='string' name='primary_genre' ordinal='22' />
            <column datatype='integer' name='cast_size' ordinal='23' />
            <column datatype='integer' name='description_words' ordinal='24' />
            <column datatype='string' name='decade_released' ordinal='25' />
            <column datatype='string' name='audience_segment' ordinal='26' />
          </columns>
        </relation>

        <metadata-records>
          <metadata-record class='capability'>
            <remote-name />
            <remote-type>0</remote-type>
            <local-name>[show_id]</local-name>
            <parent-name>[dim_titles.csv]</parent-name>
            <remote-alias />
            <ordinal>0</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
            <collation flag='0' name='LEN_US' />
          </metadata-record>
        </metadata-records>
      </connection>

      <aliases enabled='yes' />

      <!-- Calculated Fields per tableau_specs.md -->
      <column caption='Total Titles' datatype='integer' name='[Calculation_Total_Titles]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='COUNTD([show_id])' />
      </column>

      <column caption='Movie Share %' datatype='real' default-format='p0.0%' name='[Calculation_Movie_Share_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula="SUM(IF [type]='Movie' THEN 1 ELSE 0 END) / COUNTD([show_id])" />
      </column>

      <column caption='TV Share %' datatype='real' default-format='p0.0%' name='[Calculation_TV_Share_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula="SUM(IF [type]='TV Show' THEN 1 ELSE 0 END) / COUNTD([show_id])" />
      </column>

      <column caption='Fresh Content %' datatype='real' default-format='p0.0%' name='[Calculation_Fresh_Content_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='AVG([is_fresh_add])' />
      </column>

      <column caption='Avg Movie Runtime' datatype='real' default-format='n0.0 &quot;min&quot;' name='[Calculation_Avg_Movie_Runtime]' role='measure' type='quantitative'>
        <calculation class='tableau' formula="AVG(IF [type]='Movie' THEN [duration_minutes] END)" />
      </column>

      <column caption='Single-Season Show %' datatype='real' default-format='p0.0%' name='[Calculation_Single_Season_Show_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula="SUM(IF [duration_seasons]=1 THEN 1 ELSE 0 END) / SUM(IF [type]='TV Show' THEN 1 ELSE 0 END)" />
      </column>

      <column caption='Content Age Bucket' datatype='string' name='[Calculation_Content_Age_Bucket]' role='dimension' type='nominal'>
        <calculation class='tableau' formula="IF [content_age_at_add] &lt;= 0 THEN 'Day-and-date' ELSEIF [content_age_at_add] = 1 THEN '1 year' ELSEIF [content_age_at_add] &lt;= 5 THEN '2-5 years' ELSEIF [content_age_at_add] &lt;= 10 THEN '6-10 years' ELSE '10+ years' END" />
      </column>

      <!-- Field Mappings -->
      <column caption='Primary Country' datatype='string' name='[primary_country]' role='dimension' semantic-role='[Country].[ISO3166_2]' type='nominal' />
      <column caption='Country' datatype='string' name='[country]' role='dimension' semantic-role='[Country].[ISO3166_2]' type='nominal' />
      <column caption='Show Id' datatype='string' name='[show_id]' role='dimension' type='nominal' />
      <column caption='Type' datatype='string' name='[type]' role='dimension' type='nominal' />
      <column caption='Title' datatype='string' name='[title]' role='dimension' type='nominal' />
      <column caption='Director' datatype='string' name='[director]' role='dimension' type='nominal' />
      <column caption='Cast' datatype='string' name='[cast]' role='dimension' type='nominal' />
      <column caption='Date Added' datatype='date' name='[date_added]' role='dimension' type='ordinal' />
      <column caption='Release Year' datatype='integer' name='[release_year]' role='dimension' type='quantitative' />
      <column caption='Rating' datatype='string' name='[rating]' role='dimension' type='nominal' />
      <column caption='Duration' datatype='string' name='[duration]' role='dimension' type='nominal' />
      <column caption='Listed In' datatype='string' name='[listed_in]' role='dimension' type='nominal' />
      <column caption='Year Added' datatype='integer' name='[year_added]' role='dimension' type='quantitative' />
      <column caption='Month Added' datatype='integer' name='[month_added]' role='dimension' type='quantitative' />
      <column caption='Month Name Added' datatype='string' name='[month_name_added]' role='dimension' type='nominal' />
      <column caption='Quarter Added' datatype='integer' name='[quarter_added]' role='dimension' type='quantitative' />
      <column caption='Day Name Added' datatype='string' name='[day_name_added]' role='dimension' type='nominal' />
      <column caption='Duration Minutes' datatype='real' name='[duration_minutes]' role='measure' type='quantitative' />
      <column caption='Duration Seasons' datatype='integer' name='[duration_seasons]' role='measure' type='quantitative' />
      <column caption='Content Age At Add' datatype='real' name='[content_age_at_add]' role='measure' type='quantitative' />
      <column caption='Is Fresh Add' datatype='integer' name='[is_fresh_add]' role='measure' type='quantitative' />
      <column caption='Primary Genre' datatype='string' name='[primary_genre]' role='dimension' type='nominal' />
      <column caption='Cast Size' datatype='integer' name='[cast_size]' role='measure' type='quantitative' />
      <column caption='Description Words' datatype='integer' name='[description_words]' role='measure' type='quantitative' />
      <column caption='Decade Released' datatype='string' name='[decade_released]' role='dimension' type='nominal' />
      <column caption='Audience Segment' datatype='string' name='[audience_segment]' role='dimension' type='nominal' />
      <layout dim-ordering='alphabetic' dim-percentage='0.5' measure-ordering='alphabetic' measure-percentage='0.5' show-structure='true' />
    </datasource>
  </datasources>

  <worksheets>
    <!-- D1 - Executive Overview Sheets -->
    <worksheet name='KPI_Total_Titles'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10' bold='true'>TOTAL TITLES</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Text' />
            <encodings><text column='[federated.dim_titles].[cd:show_id:qk]' /></encodings>
          </pane>
        </panes>
        <rows /><cols />
      </table>
    </worksheet>

    <worksheet name='KPI_Movies'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10' bold='true'>MOVIES (69.6%)</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Text' />
            <encodings><text column='[federated.dim_titles].[cd:show_id:qk]' /></encodings>
          </pane>
        </panes>
        <rows /><cols />
      </table>
    </worksheet>

    <worksheet name='KPI_TV_Shows'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10' bold='true'>TV SHOWS (30.4%)</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Text' />
            <encodings><text column='[federated.dim_titles].[cd:show_id:qk]' /></encodings>
          </pane>
        </panes>
        <rows /><cols />
      </table>
    </worksheet>

    <worksheet name='Yearly_Additions_Combo'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Content acquisition peaked in 2019 (2,016 titles) and has disciplined since</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='integer' name='[year_added]' role='dimension' type='quantitative' />
            <column datatype='string' name='[type]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[year_added]' derivation='None' name='[none:year_added:ok]' pivot='key' type='ordinal' />
            <column-instance column='[type]' derivation='None' name='[none:type:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.dim_titles].[none:type:nk]' />
              <lod column='[federated.dim_titles].[cd:show_id:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.dim_titles].[cd:show_id:qk]</rows>
        <cols>[federated.dim_titles].[none:year_added:ok]</cols>
      </table>
    </worksheet>

    <worksheet name='Movie_vs_TV_Donut'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Movies represent 69.6% of total catalogue vs 30.4% TV Shows</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[type]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[type]' derivation='None' name='[none:type:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Pie' />
            <encodings>
              <color column='[federated.dim_titles].[none:type:nk]' />
              <size column='[federated.dim_titles].[cd:show_id:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows /><cols />
      </table>
    </worksheet>

    <worksheet name='Seasonality_Heatmap'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>July experiences peak content drops while February remains the lowest acquisition month</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='integer' name='[year_added]' role='dimension' type='quantitative' />
            <column datatype='string' name='[month_name_added]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[year_added]' derivation='None' name='[none:year_added:ok]' pivot='key' type='ordinal' />
            <column-instance column='[month_name_added]' derivation='None' name='[none:month_name_added:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Square' />
            <encodings>
              <color column='[federated.dim_titles].[cd:show_id:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.dim_titles].[none:year_added:ok]</rows>
        <cols>[federated.dim_titles].[none:month_name_added:nk]</cols>
      </table>
    </worksheet>

    <!-- D2 - Global Footprint Sheets -->
    <worksheet name='Global_Filled_Map'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>United States and India drive global catalogue volume across 120+ production markets</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[primary_country]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[primary_country]' derivation='None' name='[none:primary_country:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Automatic' />
            <encodings>
              <lod column='[federated.dim_titles].[none:primary_country:nk]' />
              <color column='[federated.dim_titles].[cd:show_id:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows /><cols />
      </table>
    </worksheet>

    <worksheet name='Top_Countries_Bar'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Top production hubs: US leads with 3,690 titles; India #2 with 1,046 titles</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[primary_country]' role='dimension' type='nominal' />
            <column datatype='string' name='[type]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[primary_country]' derivation='None' name='[none:primary_country:nk]' pivot='key' type='nominal' />
            <column-instance column='[type]' derivation='None' name='[none:type:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.dim_titles].[none:type:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.dim_titles].[none:primary_country:nk]</rows>
        <cols>[federated.dim_titles].[cd:show_id:qk]</cols>
      </table>
    </worksheet>

    <worksheet name='Butterfly_US_vs_India'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>India slate is 92% Movies vs US slate having 25.4% TV Shows — Series Opportunity Gap</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[primary_genre]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[primary_genre]' derivation='None' name='[none:primary_genre:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[none:primary_genre:nk]</rows>
        <cols>[federated.dim_titles].[cd:show_id:qk]</cols>
      </table>
    </worksheet>

    <worksheet name='Country_Summary_Table'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Market level summary: Title volume, TV share %, Adult audience %, and Avg Content Age</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[primary_country]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column datatype='real' name='[Calculation_TV_Share_Pct]' role='measure' type='quantitative' />
            <column datatype='real' name='[content_age_at_add]' role='measure' type='quantitative' />
            <column-instance column='[primary_country]' derivation='None' name='[none:primary_country:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Calculation_TV_Share_Pct]' derivation='User' name='[usr:Calculation_TV_Share_Pct:qk]' pivot='key' type='quantitative' />
            <column-instance column='[content_age_at_add]' derivation='Avg' name='[avg:content_age_at_add:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Text' />
            <encodings>
              <text column='[federated.dim_titles].[cd:show_id:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.dim_titles].[none:primary_country:nk]</rows>
        <cols />
      </table>
    </worksheet>

    <!-- D3 - Genre & Audience Sheets -->
    <worksheet name='Genre_Treemap'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>International Movies (2,752) and Dramas (2,427) constitute the largest content pillars</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[primary_genre]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[primary_genre]' derivation='None' name='[none:primary_genre:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Square' />
            <encodings>
              <size column='[federated.dim_titles].[cd:show_id:qk]' />
              <color column='[federated.dim_titles].[none:primary_genre:nk]' />
              <text column='[federated.dim_titles].[none:primary_genre:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows /><cols />
      </table>
    </worksheet>

    <worksheet name='Audience_Segment_Stacked_Bar'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Adult content (TV-MA &amp; R) commands 45.5% share; Kids &amp; Family remain under-represented (~23%)</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='integer' name='[year_added]' role='dimension' type='quantitative' />
            <column datatype='string' name='[audience_segment]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[year_added]' derivation='None' name='[none:year_added:ok]' pivot='key' type='ordinal' />
            <column-instance column='[audience_segment]' derivation='None' name='[none:audience_segment:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.dim_titles].[none:audience_segment:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.dim_titles].[cd:show_id:qk]</rows>
        <cols>[federated.dim_titles].[none:year_added:ok]</cols>
      </table>
    </worksheet>

    <worksheet name='Top_Directors_Actors'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Top Creative Talent: Rajiv Chilaka (22 dir) and Anupam Kher (43 cast) lead frequent listings</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[director]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[director]' derivation='None' name='[none:director:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[none:director:nk]</rows>
        <cols>[federated.dim_titles].[cd:show_id:qk]</cols>
      </table>
    </worksheet>

    <worksheet name='Movie_Runtime_Histogram'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Movie runtimes cluster around 90-100 minutes with a median duration of 98.0 min</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='real' name='[duration_minutes]' role='measure' type='quantitative' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[duration_minutes]' derivation='None' name='[none:duration_minutes:qk]' pivot='key' type='quantitative' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[cd:show_id:qk]</rows>
        <cols>[federated.dim_titles].[none:duration_minutes:qk]</cols>
      </table>
    </worksheet>

    <!-- D4 - Content Freshness & Series Health Sheets -->
    <worksheet name='Fresh_Content_Area'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>55% of acquisitions are fresh releases (added within 1 year of production)</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='integer' name='[year_added]' role='dimension' type='quantitative' />
            <column datatype='real' name='[Calculation_Fresh_Content_Pct]' role='measure' type='quantitative' />
            <column-instance column='[year_added]' derivation='None' name='[none:year_added:ok]' pivot='key' type='ordinal' />
            <column-instance column='[Calculation_Fresh_Content_Pct]' derivation='User' name='[usr:Calculation_Fresh_Content_Pct:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Area' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[usr:Calculation_Fresh_Content_Pct:qk]</rows>
        <cols>[federated.dim_titles].[none:year_added:ok]</cols>
      </table>
    </worksheet>

    <worksheet name='Content_Age_Buckets_Bar'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>Day-and-date &amp; 1-year releases form the dominant share of catalogue licensing</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='string' name='[Calculation_Content_Age_Bucket]' role='dimension' type='nominal' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[Calculation_Content_Age_Bucket]' derivation='None' name='[none:Calculation_Content_Age_Bucket:nk]' pivot='key' type='nominal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[cd:show_id:qk]</rows>
        <cols>[federated.dim_titles].[none:Calculation_Content_Age_Bucket:nk]</cols>
      </table>
    </worksheet>

    <worksheet name='Season_Count_Distribution_Bar'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>67.0% of TV series cancel/end after Season 1 — High early churn rate</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='integer' name='[duration_seasons]' role='measure' type='quantitative' />
            <column datatype='string' name='[show_id]' role='dimension' type='nominal' />
            <column-instance column='[duration_seasons]' derivation='None' name='[none:duration_seasons:ok]' pivot='key' type='ordinal' />
            <column-instance column='[show_id]' derivation='CountD' name='[cd:show_id:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[cd:show_id:qk]</rows>
        <cols>[federated.dim_titles].[none:duration_seasons:ok]</cols>
      </table>
    </worksheet>

    <worksheet name='TV_Share_Trend_Line'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontcolor='#F5F5F1' fontname='Arial' fontsize='12' bold='true'>TV Series share of additions increased from 25.0% (2018) to 33.7% (2021) — Pivot to Retention</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources><datasource caption='dim_titles' name='federated.dim_titles' /></datasources>
          <datasource-dependencies datasource='federated.dim_titles'>
            <column datatype='integer' name='[year_added]' role='dimension' type='quantitative' />
            <column datatype='real' name='[Calculation_TV_Share_Pct]' role='measure' type='quantitative' />
            <column-instance column='[year_added]' derivation='None' name='[none:year_added:ok]' pivot='key' type='ordinal' />
            <column-instance column='[Calculation_TV_Share_Pct]' derivation='User' name='[usr:Calculation_TV_Share_Pct:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Line' />
          </pane>
        </panes>
        <rows>[federated.dim_titles].[usr:Calculation_TV_Share_Pct:qk]</rows>
        <cols>[federated.dim_titles].[none:year_added:ok]</cols>
      </table>
    </worksheet>
  </worksheets>

  <dashboards>
    <dashboard name='1. Executive Overview'>
      <style>
        <style-rule element='dashboard'>
          <format attr='background-color' value='#141414' />
        </style-rule>
      </style>
      <size maxheight='900' maxwidth='1200' minheight='900' minwidth='1200' sizing-mode='fixed' />
      <zones>
        <zone h='900' id='1' type-name='layout-basic' w='1200' x='0' y='0'>
          <zone h='60' id='2' type-name='text' w='1160' x='20' y='20'>
            <formatted-text>
              <run fontcolor='#E50914' fontname='Arial Black' fontsize='18' bold='true'>NETFLIX CONTENT INTELLIGENCE</run>
              <run fontcolor='#F5F5F1' fontname='Arial' fontsize='16' bold='true'> | Executive Overview</run>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10'>\nStrategic Analysis of Catalogue Composition, Additions &amp; Seasonality (2008 - 2021 Snapshot)</run>
            </formatted-text>
          </zone>
          <zone h='90' id='3' name='KPI_Total_Titles' w='180' x='20' y='90' />
          <zone h='90' id='4' name='KPI_Movies' w='180' x='210' y='90' />
          <zone h='90' id='5' name='KPI_TV_Shows' w='180' x='400' y='90' />
          <zone h='350' id='9' name='Yearly_Additions_Combo' w='740' x='20' y='190' />
          <zone h='350' id='10' name='Movie_vs_TV_Donut' w='410' x='770' y='190' />
          <zone h='280' id='11' name='Seasonality_Heatmap' w='1160' x='20' y='550' />
          <zone h='30' id='12' type-name='text' w='1160' x='20' y='850'>
            <formatted-text>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='9'>Data Source: Kaggle Netflix Catalogue Snapshot (Sep 2021) | Author: Deepanshu Garkoti | LinkedIn: linkedin.com/in/deepanshugarkoti | GitHub: github.com/Deepanshu-tech7</run>
            </formatted-text>
          </zone>
        </zone>
      </zones>
    </dashboard>

    <dashboard name='2. Global Footprint'>
      <style>
        <style-rule element='dashboard'>
          <format attr='background-color' value='#141414' />
        </style-rule>
      </style>
      <size maxheight='900' maxwidth='1200' minheight='900' minwidth='1200' sizing-mode='fixed' />
      <zones>
        <zone h='900' id='21' type-name='layout-basic' w='1200' x='0' y='0'>
          <zone h='60' id='22' type-name='text' w='1160' x='20' y='20'>
            <formatted-text>
              <run fontcolor='#E50914' fontname='Arial Black' fontsize='18' bold='true'>NETFLIX CONTENT INTELLIGENCE</run>
              <run fontcolor='#F5F5F1' fontname='Arial' fontsize='16' bold='true'> | Global Footprint &amp; Slate Analysis</run>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10'>\nGlobal Distribution, Top Production Markets &amp; Regional Content Gaps</run>
            </formatted-text>
          </zone>
          <zone h='380' id='23' name='Global_Filled_Map' w='680' x='20' y='90' />
          <zone h='380' id='24' name='Top_Countries_Bar' w='470' x='710' y='90' />
          <zone h='350' id='25' name='Butterfly_US_vs_India' w='570' x='20' y='480' />
          <zone h='350' id='26' name='Country_Summary_Table' w='580' x='600' y='480' />
          <zone h='30' id='27' type-name='text' w='1160' x='20' y='850'>
            <formatted-text>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='9'>Data Source: Kaggle Netflix Catalogue Snapshot (Sep 2021) | Author: Deepanshu Garkoti | LinkedIn: linkedin.com/in/deepanshugarkoti | GitHub: github.com/Deepanshu-tech7</run>
            </formatted-text>
          </zone>
        </zone>
      </zones>
    </dashboard>

    <dashboard name='3. Genre &amp; Audience'>
      <style>
        <style-rule element='dashboard'>
          <format attr='background-color' value='#141414' />
        </style-rule>
      </style>
      <size maxheight='900' maxwidth='1200' minheight='900' minwidth='1200' sizing-mode='fixed' />
      <zones>
        <zone h='900' id='31' type-name='layout-basic' w='1200' x='0' y='0'>
          <zone h='60' id='32' type-name='text' w='1160' x='20' y='20'>
            <formatted-text>
              <run fontcolor='#E50914' fontname='Arial Black' fontsize='18' bold='true'>NETFLIX CONTENT INTELLIGENCE</run>
              <run fontcolor='#F5F5F1' fontname='Arial' fontsize='16' bold='true'> | Genre Architecture &amp; Audience</run>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10'>\nGenre Breakdown, Rating Segments, Top Talent &amp; Runtime Distribution</run>
            </formatted-text>
          </zone>
          <zone h='360' id='33' name='Genre_Treemap' w='680' x='20' y='90' />
          <zone h='360' id='34' name='Audience_Segment_Stacked_Bar' w='470' x='710' y='90' />
          <zone h='370' id='35' name='Top_Directors_Actors' w='570' x='20' y='460' />
          <zone h='370' id='36' name='Movie_Runtime_Histogram' w='580' x='600' y='460' />
          <zone h='30' id='37' type-name='text' w='1160' x='20' y='850'>
            <formatted-text>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='9'>Data Source: Kaggle Netflix Catalogue Snapshot (Sep 2021) | Author: Deepanshu Garkoti | LinkedIn: linkedin.com/in/deepanshugarkoti | GitHub: github.com/Deepanshu-tech7</run>
            </formatted-text>
          </zone>
        </zone>
      </zones>
    </dashboard>

    <dashboard name='4. Content Freshness &amp; Series Health'>
      <style>
        <style-rule element='dashboard'>
          <format attr='background-color' value='#141414' />
        </style-rule>
      </style>
      <size maxheight='900' maxwidth='1200' minheight='900' minwidth='1200' sizing-mode='fixed' />
      <zones>
        <zone h='900' id='41' type-name='layout-basic' w='1200' x='0' y='0'>
          <zone h='60' id='42' type-name='text' w='1160' x='20' y='20'>
            <formatted-text>
              <run fontcolor='#E50914' fontname='Arial Black' fontsize='18' bold='true'>NETFLIX CONTENT INTELLIGENCE</run>
              <run fontcolor='#F5F5F1' fontname='Arial' fontsize='16' bold='true'> | Freshness &amp; Series Health</run>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='10'>\nAcquisition Age, Fresh Release Ratios, Series Seasonality &amp; Renewal Survival</run>
            </formatted-text>
          </zone>
          <zone h='360' id='43' name='Fresh_Content_Area' w='570' x='20' y='90' />
          <zone h='360' id='44' name='Content_Age_Buckets_Bar' w='580' x='600' y='90' />
          <zone h='370' id='45' name='Season_Count_Distribution_Bar' w='570' x='20' y='460' />
          <zone h='370' id='46' name='TV_Share_Trend_Line' w='580' x='600' y='460' />
          <zone h='30' id='47' type-name='text' w='1160' x='20' y='850'>
            <formatted-text>
              <run fontcolor='#B3B3B3' fontname='Arial' fontsize='9'>Data Source: Kaggle Netflix Catalogue Snapshot (Sep 2021) | Author: Deepanshu Garkoti | LinkedIn: linkedin.com/in/deepanshugarkoti | GitHub: github.com/Deepanshu-tech7</run>
            </formatted-text>
          </zone>
        </zone>
      </zones>
    </dashboard>
  </dashboards>

  <windows source-height='30'>
    <!-- Worksheet Windows -->
    <window class='worksheet' name='KPI_Total_Titles'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='KPI_Movies'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='KPI_TV_Shows'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Yearly_Additions_Combo'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Movie_vs_TV_Donut'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Seasonality_Heatmap'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>

    <window class='worksheet' name='Global_Filled_Map'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Top_Countries_Bar'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Butterfly_US_vs_India'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Country_Summary_Table'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>

    <window class='worksheet' name='Genre_Treemap'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Audience_Segment_Stacked_Bar'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Top_Directors_Actors'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Movie_Runtime_Histogram'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>

    <window class='worksheet' name='Fresh_Content_Area'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Content_Age_Buckets_Bar'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='Season_Count_Distribution_Bar'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>
    <window class='worksheet' name='TV_Share_Trend_Line'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
    </window>

    <!-- Dashboard Windows with Viewpoints -->
    <window class='dashboard' maximized='true' name='1. Executive Overview'>
      <viewpoints>
        <viewpoint name='KPI_Total_Titles' />
        <viewpoint name='KPI_Movies' />
        <viewpoint name='KPI_TV_Shows' />
        <viewpoint name='Yearly_Additions_Combo' />
        <viewpoint name='Movie_vs_TV_Donut' />
        <viewpoint name='Seasonality_Heatmap' />
      </viewpoints>
      <active id='-1' />
    </window>
    <window class='dashboard' name='2. Global Footprint'>
      <viewpoints>
        <viewpoint name='Global_Filled_Map' />
        <viewpoint name='Top_Countries_Bar' />
        <viewpoint name='Butterfly_US_vs_India' />
        <viewpoint name='Country_Summary_Table' />
      </viewpoints>
      <active id='-1' />
    </window>
    <window class='dashboard' name='3. Genre &amp; Audience'>
      <viewpoints>
        <viewpoint name='Genre_Treemap' />
        <viewpoint name='Audience_Segment_Stacked_Bar' />
        <viewpoint name='Top_Directors_Actors' />
        <viewpoint name='Movie_Runtime_Histogram' />
      </viewpoints>
      <active id='-1' />
    </window>
    <window class='dashboard' name='4. Content Freshness &amp; Series Health'>
      <viewpoints>
        <viewpoint name='Fresh_Content_Area' />
        <viewpoint name='Content_Age_Buckets_Bar' />
        <viewpoint name='Season_Count_Distribution_Bar' />
        <viewpoint name='TV_Share_Trend_Line' />
      </viewpoints>
      <active id='-1' />
    </window>
  </windows>
</workbook>
"""
    ET.fromstring(twb_xml)
    return twb_xml

def build_twbx_package():
    proj_dir = r"C:\Users\Deepanshu\.gemini\antigravity-ide\scratch\netflix_analytics\netflix-analytics"
    twb_filename = "Netflix_Content_Intelligence.twb"
    twbx_filename = "Netflix_Content_Intelligence.twbx"

    twb_path = os.path.join(proj_dir, twb_filename)
    twbx_path = os.path.join(proj_dir, twbx_filename)

    xml_content = create_tableau_xml()
    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"Updated XML Workbook at: {twb_path}")

    tableau_data_dir = os.path.join(proj_dir, "tableau_data")
    with zipfile.ZipFile(twbx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(twb_path, arcname=twb_filename)

        if os.path.exists(tableau_data_dir):
            for csv_file in os.listdir(tableau_data_dir):
                if csv_file.endswith(".csv"):
                    full_csv_path = os.path.join(tableau_data_dir, csv_file)
                    zf.write(full_csv_path, arcname=csv_file)
                    zf.write(full_csv_path, arcname=os.path.join("tableau_data", csv_file))
                    zf.write(full_csv_path, arcname=os.path.join("Data", "tableau_data", csv_file))

    downloads_copy = r"C:\Users\Deepanshu\Downloads\Netflix_Content_Intelligence.twbx"
    with open(twbx_path, "rb") as sf, open(downloads_copy, "wb") as df:
        df.write(sf.read())

    print(f"Exported validated DTD-compliant .twbx to Downloads: {downloads_copy}")

if __name__ == "__main__":
    build_twbx_package()

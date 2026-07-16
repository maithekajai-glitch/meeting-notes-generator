import json
from typing import Any

import pandas as pd
import streamlit as st

from utils.ai import extract_meeting_analytics


def _show_list(
    heading: str,
    items: list[Any],
    empty_message: str,
) -> None:
    """Render a simple list inside an analytics section."""

    st.markdown(f"### {heading}")

    if not items:
        st.caption(empty_message)
        return

    for item in items:
        st.markdown(f"- {item}")


def _normalise_action_items(
    action_items: list[Any],
) -> pd.DataFrame:
    """Convert action items into a safe dataframe."""

    records: list[dict[str, str]] = []

    for item in action_items:
        if not isinstance(item, dict):
            continue

        records.append(
            {
                "Owner": str(
                    item.get("owner", "Not specified")
                ),
                "Task": str(
                    item.get("task", "Not specified")
                ),
                "Deadline": str(
                    item.get("deadline", "Not specified")
                ),
                "Priority": str(
                    item.get("priority", "Not specified")
                ),
            }
        )

    return pd.DataFrame(
        records,
        columns=[
            "Owner",
            "Task",
            "Deadline",
            "Priority",
        ],
    )


def _normalise_deadlines(
    deadlines: list[Any],
) -> pd.DataFrame:
    """Convert extracted deadlines into a dataframe."""

    records: list[dict[str, str]] = []

    for deadline in deadlines:
        if not isinstance(deadline, dict):
            continue

        records.append(
            {
                "Date / Time": str(
                    deadline.get("date", "Not specified")
                ),
                "Event": str(
                    deadline.get("event", "Not specified")
                ),
            }
        )

    return pd.DataFrame(
        records,
        columns=[
            "Date / Time",
            "Event",
        ],
    )


def analytics_section(transcript: str) -> None:
    """Display the AI Meeting Analytics Dashboard."""

    st.subheader("📊 Meeting Analytics Dashboard")

    st.caption(
        "Analyze participants, topics, decisions, action items, "
        "deadlines, risks and meeting sentiment."
    )

    if "meeting_analytics" not in st.session_state:
        st.session_state.meeting_analytics = {}

    if st.button(
        "✨ Generate Meeting Analytics",
        key="generate_meeting_analytics_button",
        use_container_width=True,
        disabled=not bool(transcript.strip()),
    ):
        try:
            with st.spinner(
                "Analyzing the meeting transcript..."
            ):
                analytics = extract_meeting_analytics(
                    transcript
                )

            st.session_state.meeting_analytics = analytics

            st.success(
                "Meeting analytics generated successfully."
            )

        except Exception as error:
            st.error(
                "The meeting analytics could not be generated. "
                "Please try again."
            )

            print(f"Meeting analytics error: {error}")

    if not transcript.strip():
        st.info(
            "Paste, upload, record, or transcribe a meeting "
            "before generating analytics."
        )
        return

    analytics = st.session_state.get(
        "meeting_analytics",
        {},
    )

    if not analytics:
        st.info(
            "Generate analytics to view the dashboard."
        )
        return

    participants = analytics.get("participants", [])
    topics = analytics.get("topics", [])
    decisions = analytics.get("decisions", [])
    action_items = analytics.get("action_items", [])
    deadlines = analytics.get("deadlines", [])
    risks = analytics.get("risks", [])
    open_questions = analytics.get(
        "open_questions",
        [],
    )

    # ---------------------------------------------
    # Summary
    # ---------------------------------------------

    with st.container(border=True):
        st.markdown("### 🧠 Meeting Overview")

        summary = analytics.get("summary", "")

        if summary:
            st.write(summary)
        else:
            st.caption("No meeting overview was generated.")

    # ---------------------------------------------
    # Main metrics
    # ---------------------------------------------

    metric_col1, metric_col2, metric_col3 = (
        st.columns(3)
    )

    with metric_col1:
        st.metric(
            "👥 Participants",
            len(participants),
        )

    with metric_col2:
        st.metric(
            "✅ Action Items",
            len(action_items),
        )

    with metric_col3:
        st.metric(
            "📌 Decisions",
            len(decisions),
        )

    metric_col4, metric_col5, metric_col6 = (
        st.columns(3)
    )

    with metric_col4:
        st.metric(
            "📅 Deadlines",
            len(deadlines),
        )

    with metric_col5:
        st.metric(
            "⚠️ Risks",
            len(risks),
        )

    with metric_col6:
        st.metric(
            "❓ Open Questions",
            len(open_questions),
        )

    # ---------------------------------------------
    # Comparison chart
    # ---------------------------------------------

    st.markdown("### 📈 Meeting Insights")

    chart_data = pd.DataFrame(
        {
            "Category": [
                "Participants",
                "Topics",
                "Decisions",
                "Action Items",
                "Deadlines",
                "Risks",
                "Open Questions",
            ],
            "Count": [
                len(participants),
                len(topics),
                len(decisions),
                len(action_items),
                len(deadlines),
                len(risks),
                len(open_questions),
            ],
        }
    ).set_index("Category")

    st.bar_chart(
        chart_data,
        use_container_width=True,
    )

    # ---------------------------------------------
    # Sentiment
    # ---------------------------------------------

    sentiment = analytics.get("sentiment", {})

    sentiment_label = str(
        sentiment.get("label", "Neutral")
    )

    sentiment_explanation = str(
        sentiment.get(
            "explanation",
            "No explanation was provided.",
        )
    )

    sentiment_icons = {
        "Positive": "🟢",
        "Neutral": "🔵",
        "Mixed": "🟡",
        "Negative": "🔴",
    }

    sentiment_icon = sentiment_icons.get(
        sentiment_label,
        "🔵",
    )

    with st.container(border=True):
        st.markdown(
            f"### {sentiment_icon} Meeting Sentiment"
        )

        st.markdown(f"**{sentiment_label}**")

        st.write(sentiment_explanation)

    # ---------------------------------------------
    # Detail tabs
    # ---------------------------------------------

    people_tab, work_tab, issues_tab = st.tabs(
        [
            "👥 People & Topics",
            "✅ Decisions & Tasks",
            "⚠️ Risks & Questions",
        ]
    )

    with people_tab:
        people_col1, people_col2 = st.columns(2)

        with people_col1:
            _show_list(
                "👥 Participants",
                participants,
                "No participant names were identified.",
            )

        with people_col2:
            _show_list(
                "💡 Main Topics",
                topics,
                "No main topics were identified.",
            )

    with work_tab:
        _show_list(
            "📌 Confirmed Decisions",
            decisions,
            "No confirmed decisions were found.",
        )

        st.markdown("### ✅ Action Items")

        action_items_df = _normalise_action_items(
            action_items
        )

        if action_items_df.empty:
            st.caption(
                "No action items were identified."
            )
        else:
            st.dataframe(
                action_items_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Owner": st.column_config.TextColumn(
                        "Owner",
                        width="medium",
                    ),
                    "Task": st.column_config.TextColumn(
                        "Task",
                        width="large",
                    ),
                    "Deadline": st.column_config.TextColumn(
                        "Deadline",
                        width="medium",
                    ),
                    "Priority": st.column_config.TextColumn(
                        "Priority",
                        width="small",
                    ),
                },
            )

        st.markdown("### 📅 Deadlines")

        deadlines_df = _normalise_deadlines(
            deadlines
        )

        if deadlines_df.empty:
            st.caption(
                "No deadlines or scheduled events were found."
            )
        else:
            st.dataframe(
                deadlines_df,
                use_container_width=True,
                hide_index=True,
            )

    with issues_tab:
        issues_col1, issues_col2 = st.columns(2)

        with issues_col1:
            _show_list(
                "⚠️ Risks and Blockers",
                risks,
                "No risks or blockers were identified.",
            )

        with issues_col2:
            _show_list(
                "❓ Open Questions",
                open_questions,
                "No open questions were identified.",
            )

    # ---------------------------------------------
    # Download
    # ---------------------------------------------

    analytics_json = json.dumps(
        analytics,
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download Analytics as JSON",
        data=analytics_json,
        file_name="meeting_analytics.json",
        mime="application/json",
        key="download_meeting_analytics_json",
        use_container_width=True,
    )
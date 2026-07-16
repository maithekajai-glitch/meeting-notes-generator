import pandas as pd
import streamlit as st

from utils.ai import extract_action_items


def action_items_section(transcript: str) -> None:
    """Display AI-extracted action items as an editable table."""

    st.subheader("✅ AI Action Items")

    st.caption(
        "Extract task owners, deadlines, priorities, and status "
        "directly from the meeting transcript."
    )

    if "action_items" not in st.session_state:
        st.session_state.action_items = []

    if st.button(
        "✨ Extract Action Items",
        key="extract_action_items_button",
        use_container_width=True,
    ):
        if not transcript.strip():
            st.warning(
                "Paste, upload, or record a meeting before "
                "extracting action items."
            )
        else:
            try:
                with st.spinner(
                    "Finding owners, tasks, and deadlines..."
                ):
                    items = extract_action_items(transcript)

                st.session_state.action_items = items

                if items:
                    st.success(
                        f"Found {len(items)} action item(s)."
                    )
                else:
                    st.info(
                        "No confirmed action items were found."
                    )

            except Exception as error:
                st.error(
                    "Action items could not be extracted. "
                    "Please try again."
                )
                print(f"Action-item extraction error: {error}")

    items = st.session_state.get("action_items", [])

    if not items:
        st.info(
            "Extracted action items will appear here."
        )
        return

    action_items_df = pd.DataFrame(
        items,
        columns=[
            "Owner",
            "Task",
            "Deadline",
            "Priority",
            "Status",
        ],
    )

    edited_df = st.data_editor(
        action_items_df,
        key="action_items_editor",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Owner": st.column_config.TextColumn(
                "Owner",
                help="Person responsible for the task",
                required=True,
            ),
            "Task": st.column_config.TextColumn(
                "Task",
                help="The required action",
                width="large",
                required=True,
            ),
            "Deadline": st.column_config.TextColumn(
                "Deadline",
                help="Deadline exactly as mentioned",
            ),
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                options=[
                    "High",
                    "Medium",
                    "Low",
                    "Not specified",
                ],
                required=True,
            ),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=[
                    "Pending",
                    "In Progress",
                    "Completed",
                    "Blocked",
                ],
                required=True,
            ),
        },
    )

    st.session_state.action_items = edited_df.to_dict(
        orient="records"
    )

    pending_count = len(
        edited_df[edited_df["Status"] == "Pending"]
    )

    completed_count = len(
        edited_df[edited_df["Status"] == "Completed"]
    )

    blocked_count = len(
        edited_df[edited_df["Status"] == "Blocked"]
    )

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric(
            "Pending",
            pending_count,
        )

    with metric_col2:
        st.metric(
            "Completed",
            completed_count,
        )

    with metric_col3:
        st.metric(
            "Blocked",
            blocked_count,
        )

    csv_data = edited_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download Action Items as CSV",
        data=csv_data,
        file_name="meeting_action_items.csv",
        mime="text/csv",
        key="download_action_items_csv",
        use_container_width=True,
    )
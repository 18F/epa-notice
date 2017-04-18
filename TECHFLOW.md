# Tech Flow

This document represents a _small_ step towards jotting down some of the
technical assumptions we have about the notice-and-comment pilot. We want to
strike a balance between flexibility and sharing expectations. As such, we
shouldn't consider this document conclusive or even necessarily up to date.

Specific attention is paid to pointing out the difference between any grand,
long-term vision and where-we-are.

## Data types/sources

### Notice meta data

Each proposed rule contains certain pieces of meta data, such as its
publication date, relevant docket numbers, and the date which comments close.
The data is published as XML in the Federal Register, though it may be too
"late" by the time it's published here for our needs. We'll generally want to
see this data before it becomes public.

_Long term_: We'd like to pull this data out of the XML automatically when
available. We also need a system for building from a hand-crafted source (when
the data's not available publicly).

_Present_: eRegs has had a need to process notices for some time -- we use
them as version identifiers, to determine effective dates, to compile changes
over time, and for section-by-section analyses (CFPB only). We _have_ a data
structure to represent these, though it may not have all of the necessary
fields. 

There is currently no way to send this metadata to the API without it being
part of the larger `pipeline` system for building regulations. There is no
mechanism in the parser to import hand-crafted notices, though we do allow
"real" notices to be modified.

There is no connection between the notice-and-comment UI and these processed
data structures. Instead, we have a configuration setting, `PREAMBLE_INTRO`,
which contains `meta` data very similar to what we're expecting we'll
eventually receive from the parser. We use this to display a special template
for the "intro" node in the preamble.

### Notice preamble

The bulk of the content for notice-and-comment comes from the "preamble" of
the notice. This section includes the "why" of the changes; we can expect the
most comments to be made in this portion. The data is published as XML in the
Federal Register (though see above for concerns about timing). We represent it
as a tree of nesting nodes the same way we represent the CFR; they only differ
in node types. Unfortunately, notices have a tendency to be numbered with a
dash, which is the character we use to join labels; as such we convert it to
an underscore.

The majority of this content comes from the "Supplementary Information"
portion of the notice XML, but a small chunk of additional data (contact
information, dates, etc.) are pulled out from other parts of the document and
packages as an "intro" node in the tree. We may have need for another custom
node to represent EPA's special instructions around submitting comments.

_Long term_: Ideally this would be part of the notice structure mentioned
above. We'd be retrieving the preamble, meta data, changes, etc. in one
request. We'd want the API to be smart enough to know that the "preamble"
portion should be stored separately and accessible via search.

_Present_: Currently, the preamble is parsed completely separately from the
notice (and the CFR data, for that matter). The UI knows to fetch the preamble
data distinct from the notice. We have no mechanism to insert an arbitrary
node as EPA's asked, though it's unclear if that's needed or if it'll be part
of the existing "Supplementary Information".

### CFR Changes

This is the "what" of a proposed rule. The preamble explains why things are
changing, but the actual contents of the change are represented differently.
The changes are written for human consumption; they are _very_ difficult to
parse. Notably, they are presented as an `<AMDPAR>` tag, with English
instructions like "6. Remove paragraph (a)(3) and add paragraph (a)(2)(iii)"
along with any _new_ text (in this case, we'd expect text for (a)(2)(iii)).

These changes are used outside of notice-and-comment to build up
"intermediate" versions of the regulation when an annual edition is not
available. We take the last good annual edition, attempt to parse the changes
present in the final rules since that edition was published, and compile the
two to generate a new version of the regulation. 

The Federal Register does not provide much context when describing CFR
changes, using asterisks as placeholders for "there is content here". It also
only provides an indication of what the text is changing _to_, not what it
was. To figure out this context and more useful change information, eRegs has
a "diff" feature, which compares two, _complete_ regulation trees and derives
the difference, which it displays to the user as a "red line" view.

Packaging all of this for notice-and-comment, we need a list of changes pulled
out from the FR notice (to pull out that `AMDPAR` text and to continue to
"compile" regulations) as well as version information (i.e. what are the "old"
and "new" versions of the reg) to pull down the relevant diffs.

_Long term_: Our parser should parse a correct list of changes and derive
appropriate version information. This data should live with the notice
structure.

_Present_: The parser knows how to pull of the correct information from
`AMDPAR`s, generate data necessary for compiling regulations, and how to build
diffs. It does _not_ know how to figure out what versions of a regulation are
relevant. Instead, we have a key in a setting, `CFR_CHANGES`, which describes
the old and new versions per CFR part.

Further, the parser does _not_ know how to package all of this data up. We
currently need to follow most of the steps in `pipeline` to generate
appropriate trees and diffs. Unfortunately, this process only account for
_final_ rules, not proposals. Despite the parser knowing how to generate the
appropriate amendment information, we don't have a system for
sending/receiving it from the API. As such, we currently use the `CFR_CHANGES`
configuration to define something very similar.

### Submission Info

To submit a comment, we need to have a valid docket number (i.e. what document
to attach this submission to) and a set of fields to request information from
a submitter. These fields may be drop-down selections, for example limiting
the user's input to a list of federal agencies. The fields may not all be
relevant to all users; as a result, we'll likely want to allow some level of
customization. The fields are generally consistent for a single agency across
multiple proposals. We should not expect fields to change over the course of a
comment period.

_Long term_: We can pull down all of this information at parse time and
include it in the notice structure. The UI would then use the data present in
this notice structure to send the comments to the correct docket and ask the
correct questions. Allowing custom templates seems like a good solution for
the hiding/modifying fields question.

_Present_: We aren't using the notice structure at all. Instead, we have a
configuration setting for `DOCUMENT_ID` to make this explicit. We have code
which fetches the appropriate field data from regulations.gov and caches it
for 24 hours. We don't do anything with customized fields.

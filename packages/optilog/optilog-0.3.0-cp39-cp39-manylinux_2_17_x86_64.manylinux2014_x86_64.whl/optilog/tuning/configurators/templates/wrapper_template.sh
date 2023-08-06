#!/usr/bin/env bash

ulimit -c 0  # Do not generate core files

CWD=$(realpath $(dirname ${0}))         # Path to the wrapper directory
SOLVER="${CWD}/algo.py"                 # Path to the solver
MATCH_TAG="${CWD}/match_tag.py"                 # Path to match_tag.py
RUNSOLVER="__@RUNSOLVER#@PATH#__"  # Path to runsolver utility
MEM_LIMIT=__@MEM#@LIMIT#__  # in MB
RUN_OBJ="__@RUN#@OBJ#__"  # quality or runtime"
CONFIGURATOR_NAME="__@CONFIGURATOR#@NAME#__"
COST_MAX="__@COST#@MAX#__"

PYTHON_EXEC="__@PYTHON#@PATH#__"

######################## Extract SMAC specific
if [[ $CONFIGURATOR_NAME == "smac" ]]; then
    INSTANCE=$1
    INSTANCE_SPECIFICS=$2
    CUTOFF=$3
    RUNLEN=$4
    SEED=$5
    shift 5
elif [[ $CONFIGURATOR_NAME == "gga" ]]; then
    INSTANCE=$1
    CUTOFF=$2
    SEED=$3
    shift 3
fi

######################## Test that the binary files exist (otherwise abort)

if [[ ! -x "${RUNSOLVER}" ]] || [[ ! -f "${RUNSOLVER}" ]]; then
    echo "${RUNSOLVER} does not exist or is not an executable" >&2
    echo "Result of this algorithm run: ABORT, 0, 0, 0, ${SEED}"
    exit -1
fi

######################## Fix parameter flags and print them

PARAMETERS=("$@")

echo "INSTANCE: $INSTANCE, SEED: $SEED"
echo "PARAMETERS: ${PARAMETERS[@]}"

######################## Run the solver using runsolver
# SMAC does not enforce the time and memory limits itself, it only tells
# the wrapper the limits' values. In this example we use runsolver to
# enforce the time and memory limits.

tmp_work_dir=`mktemp -d`
solver_file="${tmp_work_dir}/solver.txt"
time_file="${tmp_work_dir}/time.txt"

echo "Temporary output directory: ${tmp_work_dir}"
${RUNSOLVER} --watcher-data "${time_file}" --solver-data "${solver_file}"    \
             -C ${CUTOFF} -M ${MEM_LIMIT}                                    \
             "${PYTHON_EXEC}" "${SOLVER}"                                    \
             --instance "${INSTANCE}"                                        \
             --seed ${SEED}                                                  \
              ${PARAMETERS[@]}
exit_code=$?
echo "[RUNSOLVER DONE ${exit_code}]"

######################## Process the solver output and report the result

max_time=`grep "^Maximum CPU time exceeded:" "${time_file}"`
max_mem=`grep "^Maximum VSize exceeded:" "${time_file}"`

cpu_time=`grep "^CPU time (s):" "${time_file}" | cut -d ':' -f 2 | awk '{ print \$1 }'`
usr_time=`grep "^CPU user time (s):" "${time_file}" | cut -d ':' -f 2 | awk '{ print \$1 }'`
sys_time=`grep "^CPU system time (s):" "${time_file}" | cut -d ':' -f 2 | awk '{ print \$1 }'`
solver_status=`grep "^Child status:" "${time_file}" | cut -d ":" -f 2 | awk '{ print \$1 }'`



if [[ $exit_code -eq 1 ]]; then
    status="ABORT"
    quality="0"
else
    quality=${usr_time}  # we are trying to optimize the runtime.
    if [ "${RUN_OBJ}" == "quality" ]; then
        quality=`python3 "${MATCH_TAG}" "${solver_file}"`
    fi

    if [ -n "${max_mem}" ]; then
        status="MEMOUT"
    # Check timeout (i.e. max_time found and if RUN_OBJ == quality then quality is not found)
    elif [ -n "${max_time}" ] && ([ "${RUN_OBJ}" == "runtime" ] || [ -z "${quality}" ]); then
        status="TIMEOUT"
    # Check success (i.e. solver_status == 0 or RUN_OBJ == quality and quality is found)
    elif [ "${solver_status}" = "0" ] || ([ "${RUN_OBJ}" == "quality" ] && [ -n "${quality}" ]); then
        status="SUCCESS"
    # Otherwise crash
    else
        status="CRASHED"
        cat "${solver_file}"
    fi
fi

if [[ $CONFIGURATOR_NAME == "smac" ]]; then
    results="${status}, ${cpu_time}, ${RUNLEN}, ${quality}, ${SEED}, ${INSTANCE_SPECIFICS}"
    echo "Result of this algorithm run: ${results}"
elif [[ $CONFIGURATOR_NAME == "gga" ]]; then
    if [[ $status == "ABORT" ]]; then
        echo "GGA $status"
    elif [[ $status == "SUCCESS" ]]; then
        echo "GGA $status $quality"
    else
        echo "GGA $status $COST_MAX"
    fi
fi

# Check out of memory

exit ${solver_status}
